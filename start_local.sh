#!/bin/sh
cd "$(dirname "$0")" || exit 1
echo "Open http://127.0.0.1:8765/ in your browser"
exec python3 -m http.server 8765 --bind 127.0.0.1
