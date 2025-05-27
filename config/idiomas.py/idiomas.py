"""
Sistema de idiomas simplificado para Amaro Aviation Calculator v3.0
Suporte para Português e Inglês com fallbacks automáticos
"""

def get_translations():
    """Traduções centralizadas do sistema"""
    return {
        'pt': {
            # Interface Principal
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Calculadora Inteligente de Custos Operacionais',
            'language': 'Idioma',
            
            # Abas
            'tab_profit': '📈 Estimativa de Lucro Mensal',
            'tab_comparison': '⚖️ Comparativo de Custos',
            'tab_settings': '⚙️ Configurações e Fórmulas',
            
            # Campos
            'aircraft_model': 'Modelo da Aeronave',
            'monthly_hours': 'Horas de Voo por Mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo por Ano',
            'fixed_costs': 'Custos Fixos Anuais (R$)',
            'include_charter': 'Incluir Receita de Charter',
            'calculate': '🚀 Calcular',
            
            # Resultados
            'gross_revenue': 'Receita Bruta',
            'owner_revenue': 'Receita do Proprietário (90%)',
            'amaro_fee': 'Taxa Amaro (10%)',
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
            'save_settings': '💾 Salvar Configurações',
            
            # Status
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Atenção: Operação no Prejuízo',
            'settings_saved': 'Configurações salvas com sucesso!',
            'calculation_error': 'Erro no cálculo',
            
            # Exportação
            'export_excel': '📊 Baixar Excel',
            'export_pdf': '📄 Baixar PDF',
            'developed_with_love': 'Desenvolvido com ❤️ para excelência comercial'
        },
        'en': {
            # Main Interface
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Smart Operating Cost Calculator',
            'language': 'Language',
            
            # Tabs
            'tab_profit': '📈 Monthly Profit Estimation',
            'tab_comparison': '⚖️ Cost Comparison',
            'tab_settings': '⚙️ Settings & Formulas',
            
            # Fields
            'aircraft_model': 'Aircraft Model',
            'monthly_hours': 'Flight Hours per Month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs': 'Annual Fixed Costs (R$)',
            'include_charter': 'Include Charter Revenue',
            'calculate': '🚀 Calculate',
            
            # Results
            'gross_revenue': 'Gross Revenue',
            'owner_revenue': 'Owner Revenue (90%)',
            'amaro_fee': 'Amaro Fee (10%)',
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
            'save_settings': '💾 Save Settings',
            
            # Status
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Warning: Operation at Loss',
            'settings_saved': 'Settings saved successfully!',
            'calculation_error': 'Calculation error',
            
            # Export
            'export_excel': '📊 Download Excel',
            'export_pdf': '📄 Download PDF', 
            'developed_with_love': 'Developed with ❤️ for commercial excellence'
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
        selection: String selecionada ("🇧🇷 Português" ou "🇺🇸 English")
    
    Returns:
        String: 'pt' ou 'en'
    """
    return 'pt' if '🇧🇷' in selection else 'en'

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
    """Opções de idioma para selectbox"""
    return ["🇧🇷 Português", "🇺🇸 English"]

# Classe de conveniência
class LanguageManager:
    """Gerenciador de idioma simplificado"""
    
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
    # Teste do sistema
    print("=== Teste Sistema de Idiomas ===")
    print(f"PT: {get_text('app_title', 'pt')}")
    print(f"EN: {get_text('app_title', 'en')}")
    print(f"Moeda PT: {format_currency(1234.56, 'pt')}")
    print(f"Moeda EN: {format_currency(1234.56, 'en')}")
    print("✅ Sistema funcionando!")