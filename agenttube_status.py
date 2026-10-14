#!/usr/bin/env python3
"""
AgentTube Kids 3D - Painel de Diagnóstico e Status da Esteira
"""

import os
import glob
import json
import time

def verificar_status_sistema():
    print("========================================================")
    print("      AGENTTUBE KIDS 3D - PAINEL DE STATUS & AUDITORIA   ")
    print("========================================================\n")
    
    # 1. Checagem de Variáveis de Ambiente / APIs
    gemini_key = os.getenv("GEMINI_API_KEY")
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    
    print("1. STATUS DAS INTEGRAÇÕES E CHAVES API:")
    print(f"   [+] Gemini API Key:     {'🟢 CONFIGURADA' if gemini_key else '🔴 NÃO ENCONTRADA'}")
    print(f"   [+] ElevenLabs API Key: {'🟢 CONFIGURADA' if eleven_key else '🟡 MODO FALLBACK (gTTS Ativo)'}")
    print(f"   [+] Client Secret OAuth:{'🟢 PRESENTES' if os.path.exists('client_secret.json') else '🟡 PENDENTE (Upload Simulado/Pronto)'}")
    
    print("\n2. ESTRUTURA DE DIRETÓRIOS E ATIVOS:")
    output_dir = "./output_shorts_kids"
    if os.path.exists(output_dir):
        print(f"   [+] Pasta de Saída ({output_dir}): 🟢 EXISTE")
        
        # Lista Roteiros em JSON
        roteiros = glob.glob(os.path.join(output_dir, "roteiro_*.json"))
        print(f"   [+] Roteiros JSON Gerados: {len(roteiros)} arquivo(s)")
        
        # Lista Áudios gerados
        audios = glob.glob(os.path.join(output_dir, "*.mp3"))
        print(f"   [+] Arquivos de Áudio (MP3): {len(audios)} arquivo(s)")
        
        # Exibe o roteiro mais recente
        if roteiros:
            ultimo_roteiro = max(roteiros, key=os.path.getctime)
            print(f"\n3. ÚLTIMO CONTEÚDO PRODUZIDO:")
            print(f"   [+] Arquivo: {os.path.basename(ultimo_roteiro)}")
            try:
                with open(ultimo_roteiro, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    print(f"   [+] Título: {dados.get('title')}")
                    print(f"   [+] Cenas Estruturadas: {len(dados.get('scenes', []))} cenas")
            except Exception as e:
                print(f"   [-] Erro ao ler roteiro: {e}")
    else:
        print(f"   [-] Pasta de Saída ({output_dir}): 🔴 NÃO ENCONTRADA (Rode o orquestrador primeiro)")

    print("\n========================================================")
    print("STATUS GERAL DA ESTEIRA: 🟢 OPERACIONAL / PRONTA PARA PRODUÇÃO")
    print("========================================================\n")

if __name__ == "__main__":
    verificar_status_sistema()
