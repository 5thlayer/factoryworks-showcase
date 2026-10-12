#!/usr/bin/env bash
# Fails when the manifest is not what packwiz builds from the files beside it.
set -euo pipefail
cd "$(dirname "$0")/.."
packwiz refresh >/dev/null
git diff --exit-code -- pack.toml index.toml mods/
