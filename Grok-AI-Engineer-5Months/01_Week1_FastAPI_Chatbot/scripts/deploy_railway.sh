#!/usr/bin/env bash
set -euo pipefail
# Placeholder: assumes Railway CLI is configured
railway up || {
  echo "Railway CLI not configured. See README for setup.";
  exit 1;
}
