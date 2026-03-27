#!/bin/bash
# Web search using curl + Wikipedia API

QUERY="$1"
LIMIT="${2:-5}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 'search query' [limit]"
    exit 1
fi

# URL encode the query
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))" 2>/dev/null || echo "$QUERY")

echo ""
echo "🔍 Search results for: $QUERY"
echo ""

# Use Wikipedia API
curl -s "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${ENCODED_QUERY}&format=json&srlimit=${LIMIT}" \
    -H "User-Agent: OpenClawSearchBot/1.0" \
    --max-time 10 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('query', {}).get('search', [])
    for i, r in enumerate(results, 1):
        title = r.get('title', '')
        snippet = r.get('snippet', '').replace('<span class=\"searchmatch\">', '').replace('</span>', '')
        print(f'{i}. {title}')
        print(f'   https://en.wikipedia.org/wiki/{title.replace(\" \", \"_\")}')
        print(f'   {snippet[:200]}...' if len(snippet) > 200 else f'   {snippet}')
        print()
except Exception as e:
    print(f'Error: {e}')
"
