# ✈️ Amaro Aviation – Calculadora Premium de Custos & Economia

Ferramenta profissional para análise financeira em aviação executiva, desenvolvida para uso interno da Amaro Aviation e apresentações comerciais com clientes.

## 🌟 Características Premium

- **Interface Elegante**: Design profissional com identidade visual Amaro Aviation
- **Cálculos Precisos**: Sistema robusto de análise de custos operacionais
- **Modo Cliente**: Interface simplificada para apresentações comerciais
- **Exportação Profissional**: Relatórios PDF e Excel com formatação premium
- **Sistema Modular**: Arquitetura escalável e fácil manutenção
- **Configuração Flexível**: Parâmetros editáveis via interface web

## 🚀 Funcionalidades

### 📊 Dashboard Principal
- Visão geral dos modelos de aeronaves
- Métricas principais do sistema
- Comparativos automáticos de economia
- Gráficos interativos premium

### ✈️ Custo por Trecho
- Análise detalhada de rotas específicas
- Breakdown completo de custos
- Comparação com preços de mercado
- Exportação de relatórios individuais

### 📈 Projeções Mensais
- Cálculo de lucros mensais
- Simulação por horas de operação
- Análise de rentabilidade

### 🎯 Metas de Receita
- Planejamento estratégico
- Cálculo de horas necessárias para metas
- Otimização de operações

### 📊 Comparativo de Economia
- Análise anual de economia
- Comparações por modelo
- Relatórios de viabilidade

### ⚙️ Configurações Avançadas
- Edição de parâmetros operacionais
- Backup e restore de configurações
- Validação automática de dados
- Interface intuitiva com tabs organizadas

### 🎨 Modo Cliente Premium
- Interface simplificada para apresentações
- Simulador de economia personalizado
- Call-to-action profissional
- Exportação de propostas comerciais

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Local

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/amaro-calculadora.git
cd amaro-calculadora

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# 3. Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute a aplicação
streamlit run app.py
```

### Deploy no Streamlit Cloud

1. **Fork ou clone** este repositório para sua conta GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. **Conecte sua conta** GitHub
4. **Selecione o repositório** amaro-calculadora
5. **Configure**:
   - Branch: `main`
   - Main file path: `app.py`
6. **Deploy** - A aplicação estará disponível em poucos minutos

## 📁 Estrutura do Projeto

```
amaro-calculadora/
├── app.py                          # Aplicação principal
├── .streamlit/
│   └── config.toml                 # Configurações de tema
├── assets/
│   ├── logo_amaro.png              # Logo da empresa
│   └── style.css                   # Estilos personalizados
├── config/
│   └── parametros.json             # Parâmetros operacionais
├── data/
│   ├── modelos.csv                 # Dados das aeronaves
│   └── rotas.csv                   # Rotas pré-definidas
├── pages/
│   ├── 1_Custo_por_Trecho.py       # Análise por trecho
│   ├── 2_Lucros_Mensais.py         # Projeções mensais
│   ├── 3_Meta_de_Receita.py        # Planejamento de metas
│   ├── 4_Comparativo_Economia.py   # Análise comparativa
│   ├── 5_Configurações.py          # Configurações do sistema
│   └── 6_Modo_Cliente.py           # Interface para clientes
├── utils/
│   ├── calculations.py             # Lógica de cálculos
│   ├── charts.py                   # Gráficos premium
│   ├── params.py                   # Gerenciamento de parâmetros
│   ├── exportador_excel.py         # Exportação Excel
│   └── exportador_pdf.py           # Exportação PDF
├── requirements.txt                # Dependências Python
└── README.md                       # Documentação
```

## ⚙️ Configuração

### Parâmetros Operacionais

Edite via interface web (página Configurações) ou diretamente no arquivo `config/parametros.json`:

```json
{
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
```

### Modelos de Aeronaves

Adicione novos modelos no arquivo `data/modelos.csv`:

```csv
modelo,consumo_l_por_h,manut_tipo,tipo
Pilatus PC-12,260,turboprop,turboprop
Cessna Citation XLS,600,jato,jato
Embraer Phenom 300E,650,jato,jato
```

### Rotas Personalizadas

Configure rotas no arquivo `data/rotas.csv`:

```csv
origem,destino,duracao_h
GRU,SDU,1.0
GRU,CGH,0.5
CGH,BSB,1.4
BSB,SDU,1.7
```

## 🎨 Personalização Visual

### Identidade Visual
- **Cores primárias**: #8c1d40 (vermelho Amaro), #a02050 (secundário)
- **Tipografia**: Inter, Calibri, sans-serif
- **Estilo**: Moderno, limpo, profissional

### CSS Personalizado
Edite `assets/style.css` para customizar o visual:

```css
/* Métricas premium */
div[data-testid="stMetric"] {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  border-left: 5px solid #8c1d40;
}
```

## 🧪 Uso

### Para Análises Internas
1. **Dashboard**: Visão geral do sistema
2. **Custo por Trecho**: Análise detalhada de rotas
3. **Configurações**: Ajuste de parâmetros

### Para Apresentações Comerciais
1. **Modo Cliente**: Interface simplificada
2. **Simulador**: Cálculo personalizado de economia
3. **Exportação**: Relatórios profissionais

### Exemplo de Cálculo
```python
# Via código (para integração)
from utils.calculations import calcula_custo_trecho
from utils.params import load_params

params = load_params()
resultado = calcula_custo_trecho(
    modelo="Pilatus PC-12",
    duracao=1.5,
    params=params
)

print(f"Custo total: R$ {resultado['total']:,.2f}")
print(f"Economia: R$ {resultado['economia']:,.2f}")
```

## 📊 Funcionalidades Avançadas

### Sistema de Backup
- Backup automático de configurações
- Restore via interface web
- Versionamento de parâmetros

### Validação de Dados
- Verificação automática de parâmetros
- Fallbacks para arquivos corrompidos
- Mensagens de erro informativas

### Exportação Premium
- **PDF**: Relatórios com identidade visual
- **Excel**: Planilhas formatadas profissionalmente
- **Dados estruturados**: Para integrações futuras

## 🔧 Integrações Futuras

### APIs Externas
- Preços de combustível em tempo real
- Dados de voo (FlightAware)
- Cotações de mercado

### Automação
- Integração com n8n
- Webhooks para notificações
- Sincronização com CRM

### Planilhas Externas
- Google Sheets
- Excel Online
- Airtable

## 🛡️ Segurança e Backup

### Recomendações
1. **Backup regular** dos arquivos de configuração
2. **Controle de versão** para mudanças importantes
3. **Teste** em ambiente separado antes de mudanças críticas
4. **Documentação** de alterações para auditoria

### Recuperação
```bash
# Restaurar configuração padrão
cp config/parametros.json.backup config/parametros.json

# Recarregar dados
streamlit run app.py
```

## 📈 Performance

### Otimizações Implementadas
- Cache de parâmetros com `@st.cache_data`
- Carregamento lazy de dados
- Componentes otimizados
- Gráficos responsivos

### Monitoramento
- Logs de erro automáticos
- Validação de entrada
- Fallbacks robustos

## 🤝 Suporte

### Documentação
- README completo (este arquivo)
- Comentários inline no código
- Docstrings em todas as funções

### Troubleshooting
1. **Erro de parâmetros**: Verifique `config/parametros.json`
2. **Modelos ausentes**: Verifique `data/modelos.csv`
3. **Erro de importação**: Reinstale dependências

### Contato Técnico
Para suporte técnico ou melhorias:
- **Issues**: Use o GitHub Issues
- **Pull Requests**: Contribuições bem-vindas
- **Documentação**: Mantida atualizada

## 📄 Licença

Este projeto é propriedade da **Amaro Aviation** e destinado para uso interno e comercial da empresa.

## 🏆 Qualidade

### Padrões Implementados
- ✅ Código limpo e documentado
- ✅ Arquitetura modular
- ✅ Interface responsiva
- ✅ Tratamento de erros robusto
- ✅ Validação de dados
- ✅ Exportação profissional
- ✅ Identidade visual consistente

---

**Desenvolvido com ❤️ para a Amaro Aviation**  
*Excelência em Aviação Executiva*