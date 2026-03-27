import { sleep } from "baoyu-chrome-cdp";

export type SearchResult = {
  title: string;
  noteId: string;
  url: string;
  author: string;
  likes: string;
  preview: string;
};

export type NoteContent = {
  title: string;
  content: string;
  images: string[];
  author: string;
  authorId: string;
  likes: string;
  collects: string;
  comments: string;
  tags: string[];
  date: string;
  url: string;
};

export type Comment = {
  author: string;
  text: string;
  likes: string;
  replyCount: number;
  isReply: boolean;
};

/**
 * Extract search results from a XHS search page.
 * Must be called after navigating to the search URL and waiting for load.
 */
export async function extractSearchResults(
  evaluate: <T = unknown>(expr: string) => Promise<T>,
  limit: number
): Promise<SearchResult[]> {
  // Scroll to load more results
  const scrollRounds = Math.ceil(limit / 10);
  for (let i = 0; i < scrollRounds; i++) {
    await evaluate(`window.scrollBy(0, window.innerHeight)`);
    await sleep(1500);
  }

  const results = await evaluate<SearchResult[]>(`
    (() => {
      const items = [];
      // XHS search results: section containers with note cards
      const cards = document.querySelectorAll('section.note-item, [class*="note-item"], a[href*="/explore/"], a[href*="/discovery/item/"]');
      
      // Try the most common pattern first: feed-related containers
      const feedCards = document.querySelectorAll('[class*="note-item"], .feeds-page .note-item');
      const allCandidates = feedCards.length > 0 ? feedCards : cards;
      
      for (const card of allCandidates) {
        try {
          // Try to find the link to the note
          const link = card.tagName === 'A' ? card : card.querySelector('a[href*="/explore/"], a[href*="/discovery/"]');
          const href = link?.getAttribute('href') || '';
          const noteIdMatch = href.match(/\\/(?:explore|discovery\\/item)\\/([a-zA-Z0-9]+)/);
          const noteId = noteIdMatch?.[1] || '';
          
          if (!noteId) continue;
          
          // Title: look for common title elements
          const titleEl = card.querySelector('[class*="title"], .note-title, h3, .content .desc');
          const title = titleEl?.textContent?.trim() || '';
          
          // Author
          const authorEl = card.querySelector('[class*="author"], .author-wrapper .name, [class*="nickname"]');
          const author = authorEl?.textContent?.trim() || '';
          
          // Likes
          const likeEl = card.querySelector('[class*="like"], [class*="count"], .engagement .like');
          const likes = likeEl?.textContent?.trim() || '';
          
          // Preview text
          const descEl = card.querySelector('[class*="desc"], .note-desc, p');
          const preview = descEl?.textContent?.trim() || '';
          
          items.push({
            title: title || preview.slice(0, 60),
            noteId,
            url: 'https://www.xiaohongshu.com/explore/' + noteId,
            author,
            likes,
            preview: preview.slice(0, 200),
          });
        } catch {}
      }
      
      // Deduplicate by noteId
      const seen = new Set();
      return items.filter(item => {
        if (seen.has(item.noteId)) return false;
        seen.add(item.noteId);
        return true;
      });
    })()
  `);

  return (results || []).slice(0, limit);
}

/**
 * Extract search results using a more resilient approach:
 * look for all anchor tags linking to notes.
 */
export async function extractSearchResultsFallback(
  evaluate: <T = unknown>(expr: string) => Promise<T>,
  limit: number
): Promise<SearchResult[]> {
  // Scroll multiple times
  for (let i = 0; i < 5; i++) {
    await evaluate(`window.scrollBy(0, window.innerHeight)`);
    await sleep(1500);
  }

  const results = await evaluate<SearchResult[]>(`
    (() => {
      const items = [];
      const seen = new Set();
      
      // Find ALL links that point to note pages
      const allLinks = document.querySelectorAll('a[href*="/explore/"], a[href*="/search_result/"], a[href*="/discovery/item/"]');
      
      for (const link of allLinks) {
        try {
          const href = link.getAttribute('href') || '';
          const noteIdMatch = href.match(/\\/(?:explore|discovery\\/item|search_result)\\/([a-zA-Z0-9]+)/);
          const noteId = noteIdMatch?.[1] || '';
          
          if (!noteId || seen.has(noteId)) continue;
          seen.add(noteId);
          
          // Walk up to find the card container
          let container = link;
          for (let i = 0; i < 5; i++) {
            if (container.parentElement) container = container.parentElement;
            else break;
          }
          
          // Extract text from the container area
          const text = container.textContent || '';
          const imgEl = container.querySelector('img');
          const title = container.querySelector('[class*="title"], h3, .desc')?.textContent?.trim() || 
                        link.textContent?.trim() || 
                        text.slice(0, 60).trim();
          
          items.push({
            title: title,
            noteId,
            url: 'https://www.xiaohongshu.com/explore/' + noteId,
            author: '',
            likes: '',
            preview: text.slice(0, 200).trim(),
          });
        } catch {}
      }
      
      return items;
    })()
  `);

  return (results || []).slice(0, limit);
}

/**
 * Extract note content from a XHS note page.
 * Must be called after navigating to the note URL.
 */
export async function extractNoteContent(
  evaluate: <T = unknown>(expr: string) => Promise<T>,
  noteUrl: string
): Promise<NoteContent> {
  // Wait a bit more for content to render
  await sleep(2000);

  const content = await evaluate<NoteContent>(`
    (() => {
      // Title - multiple possible selectors
      const titleEl = document.querySelector('#detail-title, .title, [class*="note-title"], [class*="title"]');
      const title = titleEl?.textContent?.trim() || '';
      
      // Content text - note body
      const contentEl = document.querySelector('#detail-desc, .desc, [class*="note-text"], [class*="content"] .desc, [class*="note-content"]');
      let content = '';
      if (contentEl) {
        // Get text preserving some structure
        const cloned = contentEl.cloneNode(true);
        // Replace br with newline
        cloned.querySelectorAll('br').forEach(br => br.replaceWith('\\n'));
        content = cloned.textContent?.trim() || '';
      }
      
      // Images
      const images = [];
      // Try the swiper/carousel pattern (most common for multi-image notes)
      const swiperImgs = document.querySelectorAll('.swiper-slide img, [class*="slide"] img, .note-image img, [class*="carousel"] img');
      if (swiperImgs.length > 0) {
        for (const img of swiperImgs) {
          const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
          if (src && !src.includes('avatar') && !src.includes('emoji')) {
            images.push(src);
          }
        }
      }
      // Fallback: look for images in the main content area
      if (images.length === 0) {
        const mainImgs = document.querySelectorAll('.note-detail img, [class*="note-image"] img, .main-image img');
        for (const img of mainImgs) {
          const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
          if (src && !src.includes('avatar') && !src.includes('emoji') && !src.includes('loading')) {
            images.push(src);
          }
        }
      }
      
      // Author info
      const authorEl = document.querySelector('[class*="author"] .username, [class*="author-wrapper"] .name, .user-name, [class*="nickname"], [class*="info"] .name');
      const author = authorEl?.textContent?.trim() || '';
      
      const authorLinkEl = document.querySelector('a[href*="/user/profile/"]');
      const authorHref = authorLinkEl?.getAttribute('href') || '';
      const authorIdMatch = authorHref.match(/\\/user\\/profile\\/([a-zA-Z0-9]+)/);
      const authorId = authorIdMatch?.[1] || '';
      
      // Stats: likes, collects, comments
      // These are usually in the engagement bar at the bottom
      const statsText = document.body.innerText;
      
      const likeEl = document.querySelector('[class*="like-wrapper"] [class*="count"], [class*="like"] .count, .like-count, [class*="engageBar"] [class*="like"] span');
      const likes = likeEl?.textContent?.trim() || '';
      
      const collectEl = document.querySelector('[class*="collect-wrapper"] [class*="count"], [class*="collect"] .count, .collect-count, [class*="engageBar"] [class*="collect"] span');
      const collects = collectEl?.textContent?.trim() || '';
      
      const commentEl = document.querySelector('[class*="chat-wrapper"] [class*="count"], [class*="comment"] .count, .comment-count, [class*="engageBar"] [class*="chat"] span');
      const comments = commentEl?.textContent?.trim() || '';
      
      // Tags/hashtags
      const tags = [];
      const tagEls = document.querySelectorAll('[class*="tag"], a[href*="keyword="], .hash-tag');
      for (const tag of tagEls) {
        const text = tag.textContent?.trim();
        if (text && text.startsWith('#')) {
          tags.push(text.replace(/^#/, '').trim());
        } else if (text) {
          tags.push(text);
        }
      }
      
      // Publish date
      const dateEl = document.querySelector('[class*="date"], .publish-date, time, [class*="time"]');
      const date = dateEl?.textContent?.trim() || '';
      
      return {
        title,
        content,
        images: [...new Set(images)], // deduplicate
        author,
        authorId,
        likes,
        collects,
        comments,
        tags: [...new Set(tags)],
        date,
        url: window.location.href,
      };
    })()
  `);

  return content || {
    title: "",
    content: "",
    images: [],
    author: "",
    authorId: "",
    likes: "",
    collects: "",
    comments: "",
    tags: [],
    date: "",
    url: noteUrl,
  };
}

/**
 * Extract comments from a XHS note page.
 * Must be called after navigating to the note URL.
 * Scrolls to load more comments.
 */
export async function extractComments(
  evaluate: <T = unknown>(expr: string) => Promise<T>,
  limit: number
): Promise<Comment[]> {
  // First, scroll to the comments section
  await evaluate(`
    (() => {
      const commentSection = document.querySelector('[class*="comment"], [class*="comments-container"], #noteCommentList');
      if (commentSection) {
        commentSection.scrollIntoView({ behavior: 'smooth' });
      } else {
        // Scroll down to trigger comment loading
        window.scrollTo(0, document.body.scrollHeight * 0.6);
      }
    })()
  `);
  await sleep(2000);

  // Scroll multiple times to load more comments
  const scrollRounds = Math.min(Math.ceil(limit / 10), 10);
  for (let i = 0; i < scrollRounds; i++) {
    await evaluate(`
      (() => {
        const container = document.querySelector('[class*="comments-container"], [class*="comment-list"], #noteCommentList');
        if (container) {
          container.scrollTop = container.scrollHeight;
        } else {
          window.scrollBy(0, 600);
        }
      })()
    `);
    await sleep(1500);
  }

  const comments = await evaluate<Comment[]>(`
    (() => {
      const items = [];
      
      // Find comment items - XHS uses various patterns
      const commentItems = document.querySelectorAll(
        '[class*="comment-item"], [class*="comment-inner"], .comment-list > div, [class*="commentItem"], [id*="comment-"] '
      );
      
      for (const item of commentItems) {
        try {
          // Author
          const authorEl = item.querySelector('[class*="author"], [class*="name"], .user-name, [class*="nickname"]');
          const author = authorEl?.textContent?.trim() || '';
          
          // Comment text
          const textEl = item.querySelector('[class*="content"], [class*="text"], p');
          const text = textEl?.textContent?.trim() || '';
          
          if (!text) continue;
          
          // Likes on comment
          const likeEl = item.querySelector('[class*="like"] [class*="count"], [class*="like-count"], .like span');
          const likes = likeEl?.textContent?.trim() || '0';
          
          // Reply count
          const replyEl = item.querySelector('[class*="reply"] [class*="count"], [class*="reply-count"], .reply-btn');
          const replyText = replyEl?.textContent?.trim() || '';
          const replyCountMatch = replyText.match(/(\\d+)/);
          const replyCount = replyCountMatch ? parseInt(replyCountMatch[1]) : 0;
          
          // Is this a reply (nested comment)?
          const isReply = !!item.closest('[class*="reply-item"], [class*="sub-comment"], [class*="child-comment"]');
          
          items.push({
            author,
            text,
            likes,
            replyCount,
            isReply,
          });
        } catch {}
      }
      
      return items;
    })()
  `);

  return (comments || []).slice(0, limit);
}

/**
 * Check if the page shows a login prompt or anti-bot verification.
 */
export async function checkPageState(
  evaluate: <T = unknown>(expr: string) => Promise<T>
): Promise<"ok" | "login_required" | "verification" | "not_found"> {
  const state = await evaluate<string>(`
    (() => {
      const url = window.location.href;
      const text = document.body?.innerText || '';
      
      // Check for login redirects
      if (url.includes('/login') || url.includes('passport')) return 'login_required';
      
      // Check for verification/captcha pages
      if (text.includes('验证') && (text.includes('滑动') || text.includes('拖动'))) return 'verification';
      if (document.querySelector('[class*="captcha"], [class*="verify"]')) return 'verification';
      
      // Check for 404/not found
      if (text.includes('页面不存在') || text.includes('笔记不存在') || text.includes('404')) return 'not_found';
      
      return 'ok';
    })()
  `);

  return (state as any) || "ok";
}

/**
 * Scroll down and wait for new content to load.
 */
export async function scrollAndWait(
  evaluate: <T = unknown>(expr: string) => Promise<T>,
  rounds: number = 3,
  delayMs: number = 1500
): Promise<void> {
  for (let i = 0; i < rounds; i++) {
    await evaluate(`window.scrollBy(0, window.innerHeight)`);
    await sleep(delayMs);
  }
}
