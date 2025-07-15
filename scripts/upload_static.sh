#!/bin/sh
set -e

echo "Uploading static files to Cloudflare R2..."

rclone sync /staticfiles cloudflare-r2:bibleqna-static \
  --s3-acl public-read \
  --progress

echo "Static files uploaded, cleaning up..."
find /staticfiles -type f -delete
