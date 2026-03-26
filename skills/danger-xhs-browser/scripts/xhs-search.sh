#!/bin/bash
# XHS Search Wrapper — edits MediaCrawler config, runs search, outputs results
# Usage: xhs-search.sh "keyword" [max_notes] [with_comments]
# Example: xhs-search.sh "二十八星宿" 20 true

set -e

KEYWORD="${1:?Usage: xhs-search.sh <keyword> [max_notes] [with_comments]}"
MAX_NOTES="${2:-20}"
WITH_COMMENTS="${3:-true}"

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
MC_DIR="$WORKSPACE/MediaCrawler"
UV="$HOME/.local/bin/uv"
CONFIG="$MC_DIR/config/base_config.py"

if [ ! -d "$MC_DIR" ]; then
  echo "Error: MediaCrawler not found at $MC_DIR"
  echo "Run: cd $WORKSPACE && git clone https://github.com/NanmiCoder/MediaCrawler.git --depth 1"
  exit 1
fi

if [ ! -f "$UV" ]; then
  echo "Error: uv not found at $UV"
  echo "Run: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

echo "📝 Configuring search: keyword='$KEYWORD', max=$MAX_NOTES, comments=$WITH_COMMENTS"

# Backup config
cp "$CONFIG" "$CONFIG.bak"

# Edit config via sed
cd "$MC_DIR"

# Set keyword
sed -i '' "s/^KEYWORDS = .*/KEYWORDS = \"$KEYWORD\"/" "$CONFIG"

# Set max notes
sed -i '' "s/^CRAWLER_MAX_NOTES_COUNT = .*/CRAWLER_MAX_NOTES_COUNT = $MAX_NOTES/" "$CONFIG"

# Set save format to json
sed -i '' 's/^SAVE_DATA_OPTION = .*/SAVE_DATA_OPTION = "json"/' "$CONFIG"

# Set platform
sed -i '' 's/^PLATFORM = .*/PLATFORM = "xhs"/' "$CONFIG"

# Set crawler type
sed -i '' 's/^CRAWLER_TYPE = .*/CRAWLER_TYPE = "search"/' "$CONFIG"

# Enable CDP mode
sed -i '' 's/^ENABLE_CDP_MODE = .*/ENABLE_CDP_MODE = True/' "$CONFIG"

# Set comments
if [ "$WITH_COMMENTS" = "true" ]; then
  sed -i '' 's/^ENABLE_GET_COMMENTS = .*/ENABLE_GET_COMMENTS = True/' "$CONFIG"
  sed -i '' 's/^CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = .*/CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 20/' "$CONFIG"
else
  sed -i '' 's/^ENABLE_GET_COMMENTS = .*/ENABLE_GET_COMMENTS = False/' "$CONFIG"
fi

# Show browser (not headless) for login if needed
sed -i '' 's/^HEADLESS = .*/HEADLESS = False/' "$CONFIG"

echo "🚀 Starting MediaCrawler..."
"$UV" run python main.py --platform xhs --lt qrcode --type search 2>&1

# Find latest output
DATA_DIR="$MC_DIR/data/xhs"
if [ -d "$DATA_DIR" ]; then
  LATEST=$(ls -t "$DATA_DIR"/*.json 2>/dev/null | head -1)
  if [ -n "$LATEST" ]; then
    echo ""
    echo "✅ Data saved to: $LATEST"
    echo "📊 Records: $(python3 -c "import json; print(len(json.load(open('$LATEST'))))" 2>/dev/null || echo 'unknown')"
  fi
fi

# Restore config
mv "$CONFIG.bak" "$CONFIG"
echo "🔄 Config restored"
