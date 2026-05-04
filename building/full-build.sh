#!/bin/zsh

uv run downloader.py
uv run db-builder.py
mv output.json ../docs/data.json