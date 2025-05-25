"""
Script de inicialização - Executar antes de rodar a aplicação pela primeira vez
"""

import json
import os
import pandas as pd
from pathlib import Path

def setup_directories():
    """Cria diretórios necessários"""
    directories = ['config', 'data', 'assets', 'utils']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Diretórios criados")

def setup_config():
    """Cria arquivo de configuração padrão"""
    config_file = Path('config/parametros.json')
    
    if not config_file.exists():
        default_params = {
            "preco_combustivel": 8.66,
            "custo_piloto_hora": 1200,
            "depreciacao_anual_pct": 8,
            "custo_manutencao_hora": {
                "turboprop": 1500,
                "jato": 3000
            },
            "percentual_proprietario": 0.9,
            "preco_mercado": {
                "turboprop": 8000,
                "jato": 15000
            }
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_params, f, indent=2, ensure_ascii=False)
        
        print("✅ Arquivo de configuração criado")
    else:
        print("ℹ️ Arquivo de configuração já existe")

def setup_models():
    """Cria arquivo de modelos padrão"""
    models_file = Path('data/modelos.csv')
    
    if not models_file.exists():
        default_models = pd.DataFrame([
            {"modelo": "Pilatus PC-12", "consumo_l_por_h": 260, "manut_tipo": "turboprop", "tipo": "turboprop"},
            {"modelo": "Cessna Citation XLS", "consumo_l_por_h": 600, "manut_tipo": "jato", "tipo": "jato"},
            {"modelo": "Embraer Phenom 300E", "consumo_l_por_h": 650, "manut_tipo": "jato", "tipo": "jato"},
            {"modelo": "King Air 350", "consumo_l_por_h": 350, "manut_tipo": "turboprop", "tipo": "turboprop"},
            {"modelo": "Citation CJ3+", "consumo_l_por_h": 550, "manut_tipo": "jato", "tipo": "jato"}
        ])
        
        default_models.to_csv(models_file, index=False)
        print("✅ Arquivo de modelos criado")
    else:
        print("ℹ️ Arquivo de modelos já existe")

def setup_routes():
    """Cria arquivo de rotas padrão"""
    routes_file = Path('data/rotas.csv')
    
    if not routes_file.exists():
        default_routes = pd.DataFrame([
            {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
            {"origem": "GRU", "destino": "CGH", "duracao_h": 0.5},
            {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
            {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
            {"origem": "GRU", "destino": "VCP", "duracao_h": 0.5},
            {"origem": "CGH", "destino": "CNF", "duracao_h": 1.0},
            {"origem": "SDU", "destino": "CNF", "duracao_h": 1.0},
            {"origem": "GRU", "destino": "GIG", "duracao_h": 1.0}
        ])
        
        default_routes.to_csv(routes_file, index=False)
        print("✅ Arquivo de rotas criado")
    else:
        print("ℹ️ Arquivo de rotas já existe")

def main():
    """Executa setup completo"""
    print("🚀 Iniciando setup da Amaro Aviation Calculator...")
    print("-" * 50)
    
    setup_directories()
    setup_config()
    setup_models()
    setup_routes()
    
    print("-" * 50)
    print("✅ Setup concluído com sucesso!")
    print("\n📌 Para executar a aplicação:")
    print("   streamlit run app.py")
    print("\n📌 Para configurar parâmetros:")
    print("   Acesse a página Configurações no menu lateral")

if __name__ == "__main__":
    main()