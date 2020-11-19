#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cp data/backtickbot.service /etc/systemd/system/backtickbot.service
cp data/comment_template.css /var/www/backformat/comment_template.css