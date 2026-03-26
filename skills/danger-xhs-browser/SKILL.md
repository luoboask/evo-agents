---
name: danger-xhs-browser
description: Browse and extract content from Xiaohongshu (小红书) using MediaCrawler. Supports keyword search, note content extraction, and comment collection. Use when user mentions "小红书搜索", "抓取小红书", "小红书评论", "xhs browse", "scrape xiaohongshu", or needs to research content/comments on Xiaohongshu for competitive analysis or content strategy.
---

# XHS Browser (小红书浏览器)

Extract content from Xiaohongshu using MediaCrawler (Playwright-based). Requires user login via QR code on first use.

## ⚠️ Disclaimer

This tool uses browser automation on Xiaohongshu. Use responsibly:
- For personal learning/research only
- Respect rate limits (built-in delays)
- Do not mass-scrape or disrupt the platform

## Prerequisites

- MediaCrawler installed at: `{workspace}/MediaCrawler/`
- uv installed: `~/.local/bin/uv`
- Playwright chromium installed

If not set up, run:
```bash
cd {workspace}/MediaCrawler && ~/.local/bin/uv sync && ~/.local/bin/uv run playwright install chromium
```

## Usage

All commands run from `{workspace}/MediaCrawler/` directory.

### 1. Search Notes by Keyword

```bash
cd {workspace}/MediaCrawler
~/.local/bin/uv run python main.py --platform xhs --lt qrcode --type search
```

Before running, edit `config/base_config.py`:
- `KEYWORDS = "你要搜的关键词"` (comma-separated for multiple)
- `CRAWLER_MAX_NOTES_COUNT = 20` (number of results)
- `SAVE_DATA_OPTION = "json"` (output format)
- `ENABLE_GET_COMMENTS = True` (also grab comments)
- `ENABLE_CDP_MODE = True` (use existing Chrome login)

### 2. Get Specific Note Details

```bash
cd {workspace}/MediaCrawler
~/.local/bin/uv run python main.py --platform xhs --lt qrcode --type detail
```

Before running, edit `config/xhs_config.py`:
- `XHS_SPECIFIED_NOTE_URL_LIST` — list of note URLs (must include xsec_token)

### 3. Get Creator Profile

```bash
cd {workspace}/MediaCrawler
~/.local/bin/uv run python main.py --platform xhs --lt qrcode --type creator
```

Edit `config/xhs_config.py`:
- `XHS_CREATOR_ID_LIST` — list of creator profile URLs

## Quick Workflow (via wrapper script)

Use the wrapper script for common operations without manually editing config:

```bash
# Search
{skill_dir}/scripts/xhs-search.sh "二十八星宿" 20

# The script edits config, runs crawler, and converts output to markdown
```

## Configuration Reference

| Config Key | File | Description |
|------------|------|-------------|
| `KEYWORDS` | base_config.py | Search keywords, comma-separated |
| `CRAWLER_MAX_NOTES_COUNT` | base_config.py | Max notes to crawl |
| `ENABLE_GET_COMMENTS` | base_config.py | Enable comment crawling |
| `CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES` | base_config.py | Max comments per note |
| `ENABLE_GET_SUB_COMMENTS` | base_config.py | Enable reply crawling |
| `SAVE_DATA_OPTION` | base_config.py | json / jsonl / csv / excel |
| `ENABLE_CDP_MODE` | base_config.py | Use existing Chrome session |
| `HEADLESS` | base_config.py | False = show browser window |
| `SORT_TYPE` | xhs_config.py | popularity_descending / time_descending |
| `XHS_SPECIFIED_NOTE_URL_LIST` | xhs_config.py | Specific note URLs |
| `XHS_CREATOR_ID_LIST` | xhs_config.py | Creator profile URLs |

## Output

Data saved to `{workspace}/MediaCrawler/data/xhs/` in the configured format.

JSON output fields for notes:
- `note_id`, `title`, `desc` (full text), `type` (normal/video)
- `liked_count`, `collected_count`, `comment_count`, `share_count`
- `tag_list`, `image_list`, `video_url`
- `user_id`, `nickname`, `avatar`
- `last_update_time`

JSON output fields for comments:
- `comment_id`, `content`, `nickname`
- `liked_count`, `sub_comment_count`
- `parent_comment_id` (null if top-level)

## First-Time Login

On first run, a Chrome window opens showing a QR code. Scan with Xiaohongshu app to login. Login state is cached for subsequent runs.

If using CDP mode (`ENABLE_CDP_MODE = True`), it uses your existing Chrome browser session — no QR scan needed if you're already logged in.

## Integration with Other Skills

After extracting data, use:
- `star-mansion-master` — analyze star mansion content from search results
- `aura-content-strategist` — analyze competitor content strategies
