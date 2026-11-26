#!/usr/bin/env bash
set -euo pipefail

draft=${1:?Usage: bash scripts/blind-accept.sh <draft-name>}
current=$(atomic view list --short | sed -n 's/^\* //p')

if [[ "$current" != master ]]; then
  echo "Run this from master." >&2
  exit 1
fi

atomic insert view "$draft" --to-view master
atomic git shim reconcile
atomic git shim verify
git push origin master
atomic push storage --from-view master