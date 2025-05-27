"""
Sistema de idiomas corporativo para Amaro Aviation Calculator v3.0
Design minimalista e profissional - sem emojis ou elementos decorativos
"""

def get_translations():
    """Traduções corporativas do sistema"""
    return {
        'pt': {
            # Interface Principal
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'CALCULADORA DE CUSTOS OPERACIONAIS',
            'language': 'IDIOMA',
            
            # Abas
            'tab_profit': 'ESTIMATIVA DE LUCRO MENSAL',
            'tab_comparison': 'COMPARATIVO DE CUSTOS',
            'tab_settings': 'CONFIGURAÇÕES',
            
            # Campos
            'aircraft_model': 'Modelo da Aeronave',
            'monthly_hours': 'Horas de Voo por Mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo por Ano',
            'fixed_costs': 'Custos Fixos Anuais (R$)',
            'include_charter': 'Incluir Receita de Charter',
            'calculate': 'CALCULAR',
            
            # Resultados
            'gross_revenue': 'Receita Bruta',
            'owner_revenue': 'Receita do Proprietário',
            'amaro_fee': 'Taxa Amaro Aviation',
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Lucro Líquido',
            'monthly_roi': 'ROI Mensal',
            'own_management': 'Gestão Própria',
            'amaro_management': 'Gestão Amaro Aviation',
            'annual_savings': 'Economia Anual',
            'savings_percentage': 'Percentual de Economia',
            
            # Configurações
            'fuel_price': 'Preço do Combustível (R$/L)',
            'pilot_cost': 'Custo Piloto (R$/h)',
            'depreciation': 'Depreciação Anual (%)',
            'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
            'maintenance_jet': 'Manutenção Jato (R$/h)',
            'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
            'market_price_jet': 'Preço Mercado Jato (R$/h)',
            'save_settings': 'SALVAR CONFIGURAÇÕES',
            
            # Status
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Operação com Prejuízo',
            'settings_saved': 'Configurações salvas com sucesso',
            'calculation_error': 'Erro no cálculo',
            
            # Exportação
            'export_excel': 'EXPORTAR EXCEL',
            'export_pdf': 'EXPORTAR PDF',
            'developed_with_love': 'Desenvolvido pela Amaro Aviation'
        },
        'en': {
            # Main Interface
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'OPERATING COST CALCULATOR',
            'language': 'LANGUAGE',
            
            # Tabs
            'tab_profit': 'MONTHLY PROFIT ESTIMATION',
            'tab_comparison': 'COST COMPARISON',
            'tab_settings': 'SETTINGS',
            
            # Fields
            'aircraft_model': 'Aircraft Model',
            'monthly_hours': 'Flight Hours per Month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs': 'Annual Fixed Costs (R$)',
            'include_charter': 'Include Charter Revenue',
            'calculate': 'CALCULATE',
            
            # Results
            'gross_revenue': 'Gross Revenue',
            'owner_revenue': 'Owner Revenue',
            'amaro_fee': 'Amaro Aviation Fee',
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Profit',
            'monthly_roi': 'Monthly ROI',
            'own_management': 'Own Management',
            'amaro_management': 'Amaro Aviation Management',
            'annual_savings': 'Annual Savings',
            'savings_percentage': 'Savings Percentage',
            
            # Settings  
            'fuel_price': 'Fuel Price (R$/L)',
            'pilot_cost': 'Pilot Cost (R$/h)',
            'depreciation': 'Annual Depreciation (%)',
            'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
            'maintenance_jet': 'Jet Maintenance (R$/h)',
            'market_price_turboprop': 'Turboprop Market Price (R$/h)',
            'market_price_jet': 'Jet Market Price (R$/h)',
            'save_settings': 'SAVE SETTINGS',
            
            # Status
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Operation at Loss',
            'settings_saved': 'Settings saved successfully',
            'calculation_error': 'Calculation error',
            
            # Export
            'export_excel': 'EXPORT EXCEL',
            'export_pdf': 'EXPORT PDF', 
            'developed_with_love': 'Developed by Amaro Aviation'
        }
    }

def get_text(key, lang='pt'):
    """
    Obtém texto traduzido com fallback automático
    
    Args:
        key: Chave da tradução
        lang: Código do idioma ('pt' ou 'en')
    
    Returns:
        String traduzida ou a própria chave se não encontrada
    """
    try:
        translations = get_translations()
        return translations.get(lang, translations['pt']).get(key, key)
    except Exception:
        return key

def detect_language(selection):
    """
    Detecta idioma a partir da seleção do usuário
    
    Args:
        selection: String selecionada ("Português" ou "English")
    
    Returns:
        String: 'pt' ou 'en'
    """
    return 'pt' if selection == 'Português' else 'en'

def format_currency(value, lang='pt'):
    """
    Formata valores monetários de acordo com o idioma
    
    Args:
        value: Valor numérico
        lang: Idioma ('pt' ou 'en')
    
    Returns:
        String formatada
    """
    try:
        if lang == 'pt':
            # Formato brasileiro: R$ 1.234.567,89
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            # Formato americano: R$ 1,234,567.89
            return f"R$ {value:,.2f}"
    except Exception:
        return str(value)

def format_percentage(value, lang='pt'):
    """
    Formata percentuais de acordo com o idioma
    
    Args:
        value: Valor percentual
        lang: Idioma ('pt' ou 'en')
    
    Returns:
        String formatada
    """
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except Exception:
        return str(value)

def get_language_options():
    """Opções de idioma para selectbox - corporativo"""
    return ["Português", "English"]

# Classe de gerenciamento simplificada
class LanguageManager:
    """Gerenciador de idioma corporativo"""
    
    def __init__(self, default_lang='pt'):
        self.current_lang = default_lang
    
    def set_language(self, lang):
        """Define idioma atual"""
        if lang in ['pt', 'en']:
            self.current_lang = lang
    
    def t(self, key):
        """Traduz usando idioma atual"""
        return get_text(key, self.current_lang)
    
    def format_currency(self, value):
        """Formata moeda usando idioma atual"""
        return format_currency(value, self.current_lang)
    
    def format_percentage(self, value):
        """Formata percentual usando idioma atual"""
        return format_percentage(value, self.current_lang)

# Instância global
language_manager = LanguageManager()

# Funções de conveniência
def t(key, lang='pt'):
    """Função de conveniência para tradução"""
    return get_text(key, lang)

if __name__ == "__main__":
    # Teste corporativo do sistema
    print("=== TESTE SISTEMA DE IDIOMAS CORPORATIVO ===")
    print(f"PT: {get_text('app_title', 'pt')}")
    print(f"EN: {get_text('app_title', 'en')}")
    print(f"Moeda PT: {format_currency(1234.56, 'pt')}")
    print(f"Moeda EN: {format_currency(1234.56, 'en')}")
    print("Sistema funcionando corretamente.")