#!/bin/bash

uv venv 
source .venv/bin/activate

uv sync

# gcloud auth login --cred-file /dev/stdin  <<<"$GOOGLE_CREDENTIALS" --quiet
