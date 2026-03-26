#!/usr/bin/env python3
"""Convert MediaCrawler JSON output to readable markdown."""
import json
import sys
import os
from datetime import datetime


def notes_to_markdown(data: list, keyword: str = "") -> str:
    lines = []
    lines.append(f"# 小红书搜索结果: {keyword}")
    lines.append(f"")
    lines.append(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"笔记数量: {len(data)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, note in enumerate(data, 1):
        title = note.get("title", "无标题")
        desc = note.get("desc", "")
        nickname = note.get("nickname", "未知")
        liked = note.get("liked_count", 0)
        collected = note.get("collected_count", 0)
        comments = note.get("comment_count", 0)
        share = note.get("share_count", 0)
        note_id = note.get("note_id", "")
        note_url = note.get("note_url", f"https://www.xiaohongshu.com/explore/{note_id}")
        tags = note.get("tag_list", [])
        note_type = note.get("type", "normal")

        lines.append(f"## {i}. {title}")
        lines.append("")
        lines.append(f"**作者**: {nickname} | **类型**: {note_type}")
        lines.append(f"**互动**: 👍 {liked} | ⭐ {collected} | 💬 {comments} | 🔗 {share}")
        lines.append(f"**链接**: {note_url}")
        lines.append("")

        if desc:
            # Truncate long descriptions
            if len(desc) > 500:
                lines.append(f"> {desc[:500]}...")
            else:
                lines.append(f"> {desc}")
            lines.append("")

        if tags:
            tag_str = " ".join([f"#{t}" if isinstance(t, str) else f"#{t.get('name', '')}" for t in tags])
            lines.append(f"**标签**: {tag_str}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def comments_to_markdown(data: list, note_title: str = "") -> str:
    lines = []
    lines.append(f"# 评论: {note_title}")
    lines.append(f"")
    lines.append(f"评论数量: {len(data)}")
    lines.append("")

    for comment in data:
        nickname = comment.get("nickname", "匿名")
        content = comment.get("content", "")
        liked = comment.get("liked_count", 0)
        sub_count = comment.get("sub_comment_count", 0)
        parent_id = comment.get("parent_comment_id")

        prefix = "  ↳ " if parent_id else "- "
        lines.append(f"{prefix}**{nickname}** (👍{liked}): {content}")
        if sub_count and not parent_id:
            lines.append(f"  ({sub_count} 条回复)")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: json-to-md.py <json_file> [output_file] [--comments]")
        sys.exit(1)

    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    is_comments = "--comments" in sys.argv

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    keyword = os.path.basename(json_file).replace(".json", "").replace("_", " ")

    if is_comments:
        md = comments_to_markdown(data, keyword)
    else:
        md = notes_to_markdown(data, keyword)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Saved to {output_file}")
    else:
        print(md)


if __name__ == "__main__":
    main()
