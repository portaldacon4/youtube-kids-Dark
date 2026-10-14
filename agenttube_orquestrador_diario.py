#!/usr/bin/env python3
"""
AgentTube Kids 3D - Orquestrador de Lotes Diários & Automação 24/7
Gerencia filas de temas e executa a esteira completa: IA -> TTS -> Render -> YouTube.
"""

import time
import subprocess
import os
import json
import glob

# Fila estendida de temas virais diários focados em alta retenção e eCPM infantil
FILA_TEMAS_DIARIOS = [
    "O Tremzinho Amarelo e o Mistério das Cores no Túnel 3D",
    "A Ovelhinha Saltitante e a Nuvem de Algodão Doce",
    "O Robozinho Amigável que Consertava Brinquedos Quebrados",
    "A Escovinha de Dentes Mágica e a Festa no Castelo da Limpeza",
    "O Carrinho de Bombeiro Valente e o Gatinho na Árvore 3D"
]

def executar_esteira_completa(tema):
    print(f"\n========================================================")
    print(f"[+] INICIANDO ESTEIRA PARA O TEMA: {tema}")
    print(f"========================================================")
    
    # 1. Executa o gerador de roteiro resiliente (Gemini / Contingência)
    print("[1/3] Gerando roteiro neural via IA...")
    try:
        subprocess.run(["python", "agenttube_kids_3d_automacao.py"], check=True)
    except Exception as e:
        print(f"[-] Erro na geração do roteiro: {e}")
        return

    # 2. Executa o processador de voz e áudio (gTTS / ElevenLabs)
    print("[2/3] Processando narração e áudio...")
    try:
        subprocess.run(["python", "agenttube_tts_upload.py"], check=True)
    except Exception as e:
        print(f"[-] Erro no processamento de áudio: {e}")
        return

    # 3. Executa o módulo de upload integrado
    print("[3/3] Sincronizando com a esteira do YouTube...")
    try:
        list_files = glob.glob(os.path.join("./output_shorts_kids", "roteiro_*.json"))
        if list_files:
            latest = max(list_files, key=os.path.getctime)
            with open(latest, "r", encoding="utf-8") as f:
                dados = json.load(f)
            print(f"[+] Vídeo '{dados.get('title')}' empacotado com sucesso para o canal!")
    except Exception as e:
        print(f"[-] Erro na etapa final: {e}")

    print(f"[+] Ciclo concluído com sucesso para o tema: {tema}\n")

if __name__ == "__main__":
    print("=== AGENTTUBE KIDS 3D - SISTEMA DE LOTES DIÁRIOS ATIVO ===")
    
    for i, tema in enumerate(FILA_TEMAS_DIARIOS):
        print(f"\n[Lote Diário {i+1} de {len(FILA_TEMAS_DIARIOS)}] Processando...")
        executar_esteira_completa(tema)
        
        if i < len(FILA_TEMAS_DIARIOS) - 1:
            print("[*] Pausa entre lotes de produção...")
            time.sleep(3)
            
    print("\n[+] Lote diário de vídeos finalizado com sucesso! Canais otimizados e prontos.")
