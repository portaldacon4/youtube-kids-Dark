#!/usr/bin/env python3
"""
AgentTube Kids 3D - Autonomous YouTube Shorts Agent
Versão com Fallback Resiliente de Modelos Gemini para evitar RuntimeError.
"""

import os
import json
import time
from google import genai
from google.genai import types

CONFIG = {
    "channel_niche": "Kids 3D Nursery Rhymes & Educational Stories",
    "target_duration_seconds": 58,
    "min_ecpm_threshold_usd": 8.50,
    "animation_engine": "Blender 5.2.2 Headless",
    "voice_model": "ElevenLabs / Google TTS Fallback",
    "ai_provider": "Gemini Multi-Model Fallback",
    "output_dir": "./output_shorts_kids"
}

# Inicializa o cliente lendo a chave do ambiente
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = genai.Client()

def gerar_roteiro_e_prompt_3d(tema):
    prompt = f"""
    Crie um roteiro de YouTube Short em 3D animado (30 a 58 segundos) em Português do Brasil para o tema: '{tema}'.
    O roteiro deve seguir rigorosamente a seguinte estrutura de alta retenção infantil:
    1. Gancho Visual e Sonoro (0-5s): Pergunta curiosa ou surpresa visual colorida.
    2. Desenvolvimento dinâmico (5-40s): Aventura curta com animação 3D fofa e educativa.
    3. Loop de Retenção/Call-to-Action (40-58s): Pergunta final que incentiva o replay imediato.

    Retorne estritamente em formato JSON com a seguinte estrutura:
    {{
      "title": "Título chamativo com emojis e tags",
      "description": "Descrição otimizada com hashtags de alto RPM infantil",
      "scenes": [
        {{
          "timestamp": "0-5s",
          "prompt_3d_blender": "Descrição detalhada da cena 3D",
          "voiceover_text": "Texto da narração infantil",
          "sound_effects": "Efeitos sonoros marcantes"
        }}
      ]
    }}
    """

    # Lista abrangente de modelos para garantir resposta sem parar a automação
    modelos_candidatos = [
        'gemini-2.0-flash',
        'gemini-1.5-flash',
        'gemini-2.5-flash',
        'gemini-1.5-pro'
    ]
    
    ultimo_erro = None
    for modelo in modelos_candidatos:
        try:
            print(f"[+] Tentando gerar com o modelo: {modelo}...")
            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            if response and response.text:
                print(f"[+] Sucesso na geração com o modelo: {modelo}")
                return response.text
        except Exception as e:
            ultimo_erro = e
            print(f"[-] Modelo {modelo} indisponível ou com erro: {e}")
            continue

    # Caso nenhum modelo responda via API, gera um JSON de contingência estruturado para não quebrar a esteira 24/7
    print(f"[-] AVISO: Todos os modelos Gemini retornaram erro ({ultimo_erro}). Usando gerador de contingência local...")
    contingencia = {
        "title": f"🚗✨ {tema} | Animação Infantil 3D #Shorts",
        "description": f"Divirta-se com {tema} em animação 3D de alta qualidade! #Shorts #Infantil #Desenho3D",
        "scenes": [
            {
                "timestamp": "0-5s",
                "prompt_3d_blender": f"Cena colorida em 3D de {tema} com cores vibrantes",
                "voiceover_text": f"Você já viu {tema}? Vamos descobrir essa aventura mágica juntos!",
                "sound_effects": "Efeito sonoro mágico e risadas infantis"
            },
            {
                "timestamp": "5-40s",
                "prompt_3d_blender": "Animação fofa do personagem principal interagindo com o cenário",
                "voiceover_text": "Olha só como é divertido! Cada cantinho traz uma surpresa incrível.",
                "sound_effects": "Música alegre de fundo"
            },
            {
                "timestamp": "40-58s",
                "prompt_3d_blender": "Cena final com pergunta e animação em loop",
                "voiceover_text": "Quer ver de novo? Qual foi a sua parte favorita?",
                "sound_effects": "Som de aplausos e sininhos"
            }
        ]
    }
    return json.dumps(contingencia, ensure_ascii=False)

def criar_projeto_local():
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    config_path = os.path.join(CONFIG["output_dir"], "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=4, ensure_ascii=False)
    print(f"[+] Projeto criado em {CONFIG['output_dir']}")

def salvar_roteiro_local(roteiro_str):
    try:
        dados = json.loads(roteiro_str)
        filename = f"roteiro_{int(time.time())}.json"
        filepath = os.path.join(CONFIG["output_dir"], filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"[+] Roteiro estruturado salvo com sucesso em: {filepath}")
        return filepath
    except Exception as e:
        print(f"[-] Erro ao salvar arquivo JSON: {e}")
        return None

if __name__ == "__main__":
    print("=== AGENTTUBE KIDS 3D - MOTOR DE ROTEIRO RESILIENTE ===")
    criar_projeto_local()

    tema_exemplo = "Aventuras do Carrinho Vermelho Mágico na Fazenda 3D"
    print(f"[+] Gerando roteiro neural para: {tema_exemplo}...")

    roteiro_json = gerar_roteiro_e_prompt_3d(tema_exemplo)
    print("\n--- Roteiro Gerado com Sucesso ---")
    print(roteiro_json[:400] + "...\n")
    
    salvar_roteiro_local(roteiro_json)
