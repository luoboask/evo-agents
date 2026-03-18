#!/bin/bash
# Simple memory search using grep

QUERY="$1"
MAX_RESULTS="${2:-5}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 'search query' [max_results]"
    exit 1
fi

echo "=== Memory Search: $QUERY ==="
echo ""

# Search in memory files
count=0
for file in /Users/dhr/.openclaw/workspace/memory/*.md /Users/dhr/.openclaw/workspace/MEMORY.md; do
    if [ -f "$file" ]; then
        results=$(grep -i -n "$QUERY" "$file" 2>/dev/null | head -3)
        if [ -n "$results" ]; then
            echo "📄 $(basename $file):"
            echo "$results" | head -3
            echo ""
            ((count++))
            if [ $count -ge $MAX_RESULTS ]; then
                break
            fi
        fi
    fi
done

if [ $count -eq 0 ]; then
    echo "No results found in memory."
fi
