#!/usr/bin/env python3
"""
AgentTube Kids 3D - Módulo de Voz (ElevenLabs com Fallback gTTS) e Upload
Processa os roteiros JSON, gera o áudio sintético e realiza a integração.
"""

import os
import glob
import json
import requests
from gtts import gTTS

OUTPUT_DIR = "./output_shorts_kids"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

def pegar_ultimo_roteiro():
    list_of_files = glob.glob(os.path.join(OUTPUT_DIR, 'roteiro_*.json'))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

def gerar_voz_gtts(texto_narracao, audio_path):
    print("[+] Usando gerador gratuito de voz fallback (Google TTS)...")
    try:
        tts = gTTS(text=texto_narracao, lang='pt', slow=False)
        tts.save(audio_path)
        print(f"[+] Áudio gerado com sucesso via gTTS: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"[-] Erro no gTTS: {e}")
        return None

def gerar_voz_elevenlabs(texto_narracao):
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    audio_path = os.path.join(OUTPUT_DIR, "narracao_final.mp3")

    if api_key:
        print(f"[+] Tentando gerar narração via ElevenLabs API...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": texto_narracao,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                with open(audio_path, "wb") as f:
                    f.write(response.content)
                print(f"[+] Áudio ElevenLabs salvo com sucesso: {audio_path}")
                return audio_path
            else:
                print(f"[-] ElevenLabs informou erro de permissão/chave ({response.status_code}).")
        except Exception as e:
            print(f"[-] Falha na requisição ao ElevenLabs: {e}")

    # Fallback automático para voz gratuita
    return gerar_voz_gtts(texto_narracao, audio_path)

def simular_upload_youtube(dados_video, audio_path):
    print("\n==============================================")
    print("[+] CONECTANDO À YOUTUBE DATA API V3 (OAUTH 2.0)...")
    print("==============================================")
    print(f"Título do Short: {dados_video.get('title')}")
    print(f"Descrição: {dados_video.get('description')[:100]}...")
    print(f"Arquivo de Áudio Prontilhado: {audio_path}")
    print("[+] Status: Áudio e Roteiro vinculados e prontos para publicação!")
    print("==============================================\n")

if __name__ == "__main__":
    print("=== AGENTTUBE KIDS 3D - PROCESSADOR DE ÁUDIO E UPLOAD ===")
    
    json_path = pegar_ultimo_roteiro()
    if not json_path:
        print("[-] Nenhum roteiro JSON encontrado na pasta de saída. Execute o gerador primeiro.")
        exit()
        
    print(f"[+] Lendo o roteiro mais recente: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        roteiro = json.load(f)
        
    texto_completo = " ".join([cena["voiceover_text"] for cena in roteiro.get("scenes", [])])
    
    audio_file = gerar_voz_elevenlabs(texto_completo)
    
    if audio_file:
        simular_upload_youtube(roteiro, audio_file)
