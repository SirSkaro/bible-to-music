#!/usr/bin/env bash
set -euo pipefail

draft=$(atomic view list --short | sed -n 's/^\* //p')
case "$draft" in
  ""|master|wc/*|stash/*)
    echo "Switch to the Codex draft you reviewed first." >&2
    exit 1
    ;;
esac

atomic git shim switch master
atomic insert view "$draft" --to-view master
atomic git shim reconcile
atomic git shim verify
git push origin master
atomic push storage --from-view master