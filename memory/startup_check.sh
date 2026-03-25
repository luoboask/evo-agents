#!/bin/bash
# Daily startup check - run at the beginning of first session each day

TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)

echo "=== Daily Startup Check ==="
echo "Today: $TODAY"
echo "Yesterday: $YESTERDAY"
echo ""

# Check if today's memory file exists
if [ ! -f "/Users/dhr/.openclaw/workspace/memory/${TODAY}.md" ]; then
    echo "Creating today's memory file: memory/${TODAY}.md"
    cat > "/Users/dhr/.openclaw/workspace/memory/${TODAY}.md" << EOF
# ${TODAY} - 会话记录

## 会话

EOF
fi

# Show yesterday's memory if exists
if [ -f "/Users/dhr/.openclaw/workspace/memory/${YESTERDAY}.md" ]; then
    echo "=== Yesterday's Summary ==="
    head -50 "/Users/dhr/.openclaw/workspace/memory/${YESTERDAY}.md"
    echo ""
    echo "(Full file: memory/${YESTERDAY}.md)"
else
    echo "No memory file for yesterday (${YESTERDAY})"
fi

echo ""
echo "=== Ready ==="
