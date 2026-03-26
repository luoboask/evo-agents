import type { SearchResult, NoteContent, Comment } from "./extract.js";

/**
 * Format search results as a markdown document.
 */
export function formatSearchResultsMarkdown(
  keyword: string,
  results: SearchResult[]
): string {
  const lines: string[] = [];

  lines.push("---");
  lines.push(`keyword: ${JSON.stringify(keyword)}`);
  lines.push(`resultCount: ${results.length}`);
  lines.push(`date: ${JSON.stringify(new Date().toISOString())}`);
  lines.push("---");
  lines.push("");
  lines.push(`# 小红书搜索: ${keyword}`);
  lines.push("");
  lines.push(`共 ${results.length} 条结果`);
  lines.push("");

  if (results.length === 0) {
    lines.push("_没有找到相关笔记_");
    return lines.join("\n");
  }

  // Format as a list (more readable and compatible)
  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    lines.push(`### ${i + 1}. ${r.title || "(无标题)"}`);
    lines.push("");
    if (r.author) lines.push(`- **作者**: ${r.author}`);
    if (r.likes) lines.push(`- **点赞**: ${r.likes}`);
    if (r.preview) lines.push(`- **预览**: ${r.preview}`);
    lines.push(`- **链接**: ${r.url}`);
    lines.push(`- **ID**: \`${r.noteId}\``);
    lines.push("");
  }

  return lines.join("\n");
}

/**
 * Format note content as markdown with YAML front matter.
 */
export function formatNoteMarkdown(note: NoteContent): string {
  const lines: string[] = [];

  // YAML front matter
  lines.push("---");
  lines.push(`url: ${JSON.stringify(note.url)}`);
  if (note.title) lines.push(`title: ${JSON.stringify(note.title)}`);
  if (note.author) lines.push(`author: ${JSON.stringify(note.author)}`);
  if (note.authorId) lines.push(`authorId: ${JSON.stringify(note.authorId)}`);
  if (note.likes) lines.push(`likes: ${JSON.stringify(note.likes)}`);
  if (note.collects) lines.push(`collects: ${JSON.stringify(note.collects)}`);
  if (note.comments) lines.push(`comments: ${JSON.stringify(note.comments)}`);
  if (note.date) lines.push(`date: ${JSON.stringify(note.date)}`);
  if (note.tags.length > 0) {
    lines.push(`tags: [${note.tags.map((t) => JSON.stringify(t)).join(", ")}]`);
  }
  lines.push(`extractedAt: ${JSON.stringify(new Date().toISOString())}`);
  lines.push("---");
  lines.push("");

  // Title
  if (note.title) {
    lines.push(`# ${note.title}`);
    lines.push("");
  }

  // Author info
  if (note.author) {
    lines.push(`> 作者: **${note.author}**`);
    if (note.date) {
      lines.push(`> 发布于: ${note.date}`);
    }
    lines.push("");
  }

  // Content body
  if (note.content) {
    lines.push(note.content);
    lines.push("");
  }

  // Tags
  if (note.tags.length > 0) {
    lines.push("## 标签");
    lines.push("");
    lines.push(note.tags.map((t) => `#${t}`).join(" "));
    lines.push("");
  }

  // Images
  if (note.images.length > 0) {
    lines.push("## 图片");
    lines.push("");
    for (let i = 0; i < note.images.length; i++) {
      lines.push(`![图${i + 1}](${note.images[i]})`);
      lines.push("");
    }
  }

  // Stats
  const stats: string[] = [];
  if (note.likes) stats.push(`❤️ ${note.likes}`);
  if (note.collects) stats.push(`⭐ ${note.collects}`);
  if (note.comments) stats.push(`💬 ${note.comments}`);
  if (stats.length > 0) {
    lines.push("---");
    lines.push("");
    lines.push(stats.join(" | "));
    lines.push("");
  }

  return lines.join("\n");
}

/**
 * Format comments as a markdown document.
 */
export function formatCommentsMarkdown(
  noteId: string,
  noteUrl: string,
  comments: Comment[]
): string {
  const lines: string[] = [];

  lines.push("---");
  lines.push(`noteUrl: ${JSON.stringify(noteUrl)}`);
  lines.push(`noteId: ${JSON.stringify(noteId)}`);
  lines.push(`commentCount: ${comments.length}`);
  lines.push(`extractedAt: ${JSON.stringify(new Date().toISOString())}`);
  lines.push("---");
  lines.push("");
  lines.push(`# 评论 - ${noteId}`);
  lines.push("");
  lines.push(`共 ${comments.length} 条评论`);
  lines.push("");

  if (comments.length === 0) {
    lines.push("_暂无评论_");
    return lines.join("\n");
  }

  for (const c of comments) {
    const prefix = c.isReply ? "  - " : "- ";
    const authorPart = c.author ? `**${c.author}**` : "匿名";
    const likePart = c.likes && c.likes !== "0" ? ` (❤️ ${c.likes})` : "";
    const replyPart = c.replyCount > 0 ? ` [${c.replyCount} 条回复]` : "";

    lines.push(`${prefix}${authorPart}${likePart}${replyPart}`);
    lines.push(`${prefix.replace("-", " ")} ${c.text}`);
    lines.push("");
  }

  return lines.join("\n");
}
