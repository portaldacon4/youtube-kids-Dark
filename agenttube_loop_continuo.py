#!/usr/bin/env python3
"""
AgentTube Kids 3D - Loop de Automação Contínua 24/7
Gerencia filas de temas e executa a produção automatizada em lotes diários.
"""

import time
import subprocess
import os

# Fila de temas estratégicos de alta demanda e RPM para o canal infantil
TEMAS_KIDS = [
    "Aventuras do Carrinho Vermelho Mágico na Fazenda 3D",
    "O Ursinho Curioso e a Floresta das Cores Perdidas",
    "A Estrelinha Brilhante que Queria Voar na Lua",
    "O Robozinho Dançarino na Fábrica de Brinquedos",
    "O Pinguim Astronauta e o Gelo Musical"
]

def executar_ciclo_producao(tema):
    print(f"\n==============================================")
    print(f"[+] INICIANDO NOVO CICLO DE PRODUÇÃO: {tema}")
    print(f"==============================================")
    
    # Define a variável de tema temporariamente ou chama o script principal
    # Aqui simulamos a chamada do script de roteiro/Blender ajustado
    try:
        # Executa o script de geração criado anteriormente
        resultado = subprocess.run(
            ["python", "agenttube_kids_3d_automacao.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print(resultado.stdout)
        print(f"[+] Ciclo concluído com sucesso para o tema: {tema}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Erro na execução do ciclo: {e.stderr}")

if __name__ == "__main__":
    print("=== AGENTTUBE KIDS 3D - MOTOR DE AUTOMAÇÃO CONTÍNUA ATIVO ===")
    
    # Modo de Loop Contínuo (Exemplo: Executa 1 vídeo a cada 24 horas ou sob demanda)
    # Para testes imediatos, rodamos a lista uma vez. Para 24/7, mantenha o while True com sleep.
    for i, tema in enumerate(TEMAS_KIDS):
        print(f"\n[Fila {i+1}/{len(TEMAS_KIDS)}] Processando...")
        executar_ciclo_producao(tema)
        
        if i < len(TEMAS_KIDS) - 1:
            print("[*] Aguardando intervalo programado para o próximo lote (Modo 24/7)...")
            # time.sleep(86400) # Descomente para rodar a cada 24 horas reais
            time.sleep(5)     # Pausa curta apenas para demonstração em lote
            
    print("\n[+] Lote diário de automação finalizado com sucesso!")
