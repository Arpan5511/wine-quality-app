#!/usr/bin/env bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt

echo "Build complete!"
