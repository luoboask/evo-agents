#!/bin/bash
# Simple memory search using rg

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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
for file in "${WORKSPACE_ROOT}"/memory/*.md "${WORKSPACE_ROOT}"/MEMORY.md; do
    if [ -f "$file" ]; then
        results=$(rg -i -n --max-count 3 "$QUERY" "$file" 2>/dev/null)
        if [ -n "$results" ]; then
            echo "📄 $(basename $file):"
            echo "$results"
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
