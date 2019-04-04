#!/usr/bin/env zsh
docker run --rm -d -v ~/workspace/data:/data/db -p 27017:27017/tcp mongo:latest