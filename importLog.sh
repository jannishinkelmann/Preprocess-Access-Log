#!/bin/bash

# Config
PROCESS_SCRIPT_PATH="./processLog.py"
IMPORT_SCRIPT_PATH="./Matomo/misc/log-analytics/import_logs.py"
DOMAINS="example.com www.example.com"
MATOMO_URL="https://analytics.example.com"
MATOMO_USER="matomo_admin"
MATOMO_PASS="SECRET"
MATOMO_SITE_ID="1"
MATOMO_OPTIONS="--enable-http-errors --enable-http-redirects --enable-static --enable-bots"

# Constants
TMP_FILE_NAME="access_log_tmp"

# Procedure
if [ -e "$TMP_FILE_NAME" ]
then
        echo "Unable to write temp file. File $TMP_FILE_NAME does already exist."
        return
fi
python "$PROCESS_SCRIPT_PATH" -a "$1" "$TMP_FILE_NAME" "$DOMAINS"
python "$IMPORT_SCRIPT_PATH" --url="$MATOMO_URL" --login="$MATOMO_USER" --password="$MATOMO_PASS" --idsite="$MATOMO_SITE_ID" "$MATOMO_OPTIONS" "$TMP_FILE_NAME"
rm "$TMP_FILE_NAME"
