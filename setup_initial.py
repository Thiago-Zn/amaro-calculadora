"""
Script de configuração inicial para Amaro Aviation Calculator v3.0
Versão simplificada e robusta para setup automático
"""

import json
import os
import pandas as pd
from pathlib import Path
import sys

def print_header():
    """Exibe cabeçalho do setup"""
    print("="*60)
    print("✈️  AMARO AVIATION CALCULATOR v3.0")
    print("    Setup e Configuração Inicial")
    print("="*60)
    print()

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"🐍 Verificando Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERRO: Python 3.8+ é necessário")
        print("   Versão atual:", f"{version.major}.{version.minor}.{version.micro}")
        print("   Por favor, atualize o Python e tente novamente")
        return False
    
    print("✅ Versão do Python OK")
    return True

def create_directories():
    """Cria estrutura de diretórios necessária"""
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        'config',
        'data', 
        'assets',
        'utils',
        '.streamlit'
    ]
    
    created_count = 0
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📂 Criado: {directory}/")
            created_count += 1
        else:
            print(f"   ✅ Existe: {directory}/")
    
    print(f"✅ Estrutura criada ({created_count} novos diretórios)")
    return True

def create_default_config():
    """Cria arquivo de configuração padrão"""
    print("\n⚙️ Configurando parâmetros padrão...")
    
    config_file = Path('config/parametros.json')
    
    default_config = {
        "preco_combustivel": 8.66,
        "custo_piloto_hora": 1200,
        "depreciacao_anual_pct": 8.0,
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
    
    try:
        if config_file.exists():
            print("   ℹ️  Arquivo de configuração já existe")
            
            # Verificar se precisa atualizar
            with open(config_file, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
            
            # Adicionar chaves ausentes
            updated = False
            for key, value in default_config.items():
                if key not in existing_config:
                    existing_config[key] = value
                    updated = True
                    print(f"   ➕ Adicionado: {key}")
            
            if updated:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_config, f, indent=2, ensure_ascii=False)
                print("   🔄 Configuração atualizada")
            else:
                print("   ✅ Configuração está atualizada")
        else:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print("   ✅ Configuração padrão criada")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar configuração: {e}")
        return False

def create_aircraft_models():
    """Cria arquivo de modelos de aeronaves"""
    print("\n✈️ Configurando modelos de aeronaves...")
    
    models_file = Path('data/modelos.csv')
    
    default_models = pd.DataFrame([
        {
            "modelo": "Pilatus PC-12", 
            "consumo_l_por_h": 260, 
            "manut_tipo": "turboprop", 
            "tipo": "turboprop"
        },
        {
            "modelo": "Cessna Citation XLS", 
            "consumo_l_por_h": 600, 
            "manut_tipo": "jato", 
            "tipo": "jato"
        },
        {
            "modelo": "Embraer Phenom 300E", 
            "consumo_l_por_h": 650, 
            "manut_tipo": "jato", 
            "tipo": "jato"
        },
        {
            "modelo": "King Air 350", 
            "consumo_l_por_h": 350, 
            "manut_tipo": "turboprop", 
            "tipo": "turboprop"
        },
        {
            "modelo": "Citation CJ3+", 
            "consumo_l_por_h": 550, 
            "manut_tipo": "jato", 
            "tipo": "jato"
        }
    ])
    
    try:
        if models_file.exists():
            print("   ℹ️  Arquivo de modelos já existe")
            
            # Verificar se tem dados válidos
            existing_models = pd.read_csv(models_file)
            if len(existing_models) == 0:
                default_models.to_csv(models_file, index=False)
                print("   🔄 Modelos padrão adicionados (arquivo estava vazio)")
            else:
                print(f"   ✅ {len(existing_models)} modelos configurados")
        else:
            default_models.to_csv(models_file, index=False)
            print(f"   ✅ {len(default_models)} modelos padrão criados")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar modelos: {e}")
        return False

def create_routes():
    """Cria arquivo de rotas padrão"""
    print("\n🗺️ Configurando rotas padrão...")
    
    routes_file = Path('data/rotas.csv')
    
    default_routes = pd.DataFrame([
        {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
        {"origem": "GRU", "destino": "CGH", "duracao_h": 0.5},
        {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
        {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
        {"origem": "GRU", "destino": "CNF", "duracao_h": 1.0},
        {"origem": "SDU", "destino": "CNF", "duracao_h": 1.0},
        {"origem": "GIG", "destino": "BSB", "duracao_h": 1.5},
        {"origem": "CGH", "destino": "CWB", "duracao_h": 1.0}
    ])
    
    try:
        if routes_file.exists():
            print("   ℹ️  Arquivo de rotas já existe")
            existing_routes = pd.read_csv(routes_file)
            print(f"   ✅ {len(existing_routes)} rotas configuradas")
        else:
            default_routes.to_csv(routes_file, index=False)
            print(f"   ✅ {len(default_routes)} rotas padrão criadas")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar rotas: {e}")
        return False

def create_streamlit_config():
    """Cria configuração do Streamlit"""
    print("\n🎨 Configurando tema Streamlit...")
    
    config_file = Path('.streamlit/config.toml')
    
    streamlit_config = """[theme]
base = "light"
primaryColor = "#8c1d40"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
enableCORS = false
enableXsrfProtection = false
"""
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(streamlit_config)
        print("   ✅ Tema Amaro Aviation configurado")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao configurar Streamlit: {e}")
        return False

def check_dependencies():
    """Verifica dependências principais"""
    print("\n📦 Checando dependências principais...")
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('plotly', 'plotly'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} (não instalado)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Pacotes ausentes: {', '.join(missing_packages)}")
        print("   Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências principais estão instaladas")
    return True

def create_requirements_file():
    """Cria arquivo requirements.txt se não existir"""
    print("\n📋 Verificando requirements.txt...")
    
    requirements_file = Path('requirements.txt')
    
    requirements_content = """# Amaro Aviation Calculator v3.0 - Dependencies
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
reportlab>=4.0.0
Pillow>=10.0.0
python-dateutil>=2.8.0
"""
    
    try:
        if not requirements_file.exists():
            with open(requirements_file, 'w', encoding='utf-8') as f:
                f.write(requirements_content)
            print("   ✅ requirements.txt criado")
        else:
            print("   ℹ️  requirements.txt já existe")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar requirements.txt: {e}")
        return False

def test_configuration():
    """Testa se a configuração está funcionando"""
    print("\n🧪 Testando configuração...")
    
    try:
        # Testar carregamento de parâmetros
        from utils.params import load_params
        params = load_params()
        print(f"   ✅ Parâmetros carregados ({len(params)} chaves)")
        
        # Testar modelos
        modelos = params.get('modelos_disponiveis', [])
        print(f"   ✅ Modelos disponíveis: {len(modelos)}")
        
        # Testar cálculo básico
        if modelos:
            from utils.calculations import calcula_custo_trecho
            resultado = calcula_custo_trecho(modelos[0], 1.0, params)
            print(f"   ✅ Cálculo de teste: R$ {resultado['total']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste de configuração: {e}")
        print(f"   💡 Detalhes: {str(e)}")
        return False

def show_next_steps():
    """Mostra próximos passos após instalação"""
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print()
    print("📌 PRÓXIMOS PASSOS:")
    print()
    print("1. 🚀 Executar a aplicação:")
    print("   streamlit run app.py")
    print()
    print("2. 🌐 Acessar no navegador:")
    print("   http://localhost:8501")
    print()
    print("3. 🎯 Para uso comercial:")
    print("   • Ajuste parâmetros na aba 'Configurações'")
    print("   • Adicione modelos personalizados em 'data/modelos.csv'")
    print("   • Configure rotas em 'data/rotas.csv'")
    print()
    print("4. 📊 Para desenvolvimento:")
    print("   • Execute testes: python -m pytest tests/")
    print("   • Ative debug: streamlit run app.py --logger.level=debug")
    print()
    print("💡 DICAS:")
    print("   • Use F11 para modo tela cheia em apresentações")
    print("   • Exporte relatórios usando os botões de download")
    print("   • Configure backup automático dos parâmetros")
    print()
    print("📞 SUPORTE:")
    print("   • Documentação: README_Refatorado.md")
    print("   • Email: suporte@amaroaviation.com")
    print("   • GitHub Issues: Para bugs e sugestões")
    print()
    print("-" * 60)
    print("✈️  Amaro Aviation - Excelência em Aviação Executiva")
    print("-" * 60)

def main():
    """Função principal do setup"""
    print_header()
    
    success_steps = 0
    total_steps = 8
    
    # Lista de passos do setup
    steps = [
        ("Verificação do Python", check_python_version),
        ("Criação de diretórios", create_directories),
        ("Configuração padrão", create_default_config),
        ("Modelos de aeronaves", create_aircraft_models),
        ("Rotas padrão", create_routes),
        ("Configuração Streamlit", create_streamlit_config),
        ("Arquivo requirements.txt", create_requirements_file),
        ("Teste de configuração", test_configuration)
    ]
    
    # Executar cada passo
    for step_name, step_function in steps:
        try:
            if step_function():
                success_steps += 1
            else:
                print(f"⚠️  Falha em: {step_name}")
        except Exception as e:
            print(f"❌ Erro crítico em {step_name}: {e}")
    
    print(f"\n📊 RESUMO: {success_steps}/{total_steps} passos concluídos")
    
    if success_steps == total_steps:
        print("✅ Setup 100% concluído!")
        show_next_steps()
    elif success_steps >= total_steps - 1:
        print("⚠️  Setup quase completo com advertências menores")
        print("   A aplicação deve funcionar normalmente")
        show_next_steps()
    else:
        print("❌ Setup incompleto - alguns problemas precisam ser resolvidos")
        print("   Verifique os erros acima e execute novamente")
        print()
        print("💡 Soluções comuns:")
        print("   • Instalar dependências: pip install -r requirements.txt")
        print("   • Verificar permissões de escrita nos diretórios")
        print("   • Executar como administrador se necessário")

def quick_setup():
    """Setup rápido sem interação do usuário"""
    print("🚀 SETUP RÁPIDO - SEM INTERAÇÃO")
    print("-" * 40)
    
    # Setup mínimo necessário
    minimal_steps = [
        create_directories,
        create_default_config,
        create_aircraft_models,
        create_streamlit_config
    ]
    
    for step in minimal_steps:
        try:
            step()
        except Exception as e:
            print(f"Erro no setup rápido: {e}")
            return False
    
    print("✅ Setup rápido concluído!")
    print("Execute: streamlit run app.py")
    return True

if __name__ == "__main__":
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_setup()
    else:
        main()