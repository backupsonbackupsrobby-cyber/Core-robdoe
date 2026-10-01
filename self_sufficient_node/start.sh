#!/usr/bin/env bash
# Ensure Redis caching instance is fully awake locally
redis-server --daemonize yes 2>/dev/null
# Run execution layer
node server.js
