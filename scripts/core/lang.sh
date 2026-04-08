#!/bin/bash
# lang.sh - Language detection helper
# Source this file in other scripts to get LANG variable set
# Usage: source lang.sh

# Detect system language (default: English)
if locale | grep -q "zh_CN\|zh_CN\|Chinese"; then
    LANG="zh"
else
    LANG="en"
fi
