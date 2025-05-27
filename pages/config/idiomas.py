"""
Sistema de idiomas centralizado para Amaro Aviation Calculator
Suporte completo para Português e Inglês
"""

TRANSLATIONS = {
    # Português (Brasil)
    'pt': {
        # Interface Principal
        'app_title': 'Amaro Aviation',
        'app_subtitle': 'Calculadora Inteligente de Custos Operacionais',
        'language_selector': '🌐 Idioma',
        
        # Navegação e Abas
        'tab_monthly_profit': '📈 Estimativa de Lucro Mensal',
        'tab_cost_comparison': '⚖️ Comparativo de Custos',
        'tab_settings': '⚙️ Configurações e Fórmulas',
        
        # Campos de Entrada
        'aircraft_model': 'Modelo da Aeronave',
        'flight_hours_month': 'Horas de Voo por Mês',
        'occupancy_rate': 'Taxa de Ocupação (%)',
        'annual_hours': 'Horas de Voo por Ano',
        'fixed_costs_annual': 'Custos Fixos Anuais (R$)',
        'include_charter_revenue': 'Incluir Receita de Charter',
        
        # Botões
        'calculate': '🚀 Calcular',
        'save_settings': '💾 Salvar Configurações',
        'reload_data': '🔄 Recarregar Dados',
        'presentation_mode': '📱 Modo Apresentação',
        'export_excel': '📊 Baixar Relatório Excel',
        'export_pdf': '📄 Baixar Relatório PDF',
        'export_text': '📄 Baixar Relatório Texto',
        
        # Resultados - Lucro Mensal
        'gross_revenue': 'Receita Bruta',
        'owner_share': 'Receita do Proprietário',
        'amaro_share': 'Taxa Amaro Aviation',
        'operational_costs': 'Custos Operacionais',
        'net_profit': 'Lucro Líquido',
        'monthly_roi': 'ROI Mensal',
        'projected_annual_revenue': 'Receita Anual Projetada',
        
        # Resultados - Comparativo
        'own_management': 'Gestão Própria',
        'amaro_management': 'Gestão Amaro Aviation',
        'annual_savings': 'Economia Anual',
        'monthly_savings': 'Economia Mensal',
        'savings_percentage': 'Percentual de Economia',
        'fixed_costs': 'Custos Fixos',
        'variable_costs': 'Custos Variáveis',
        'charter_revenue': 'Receita Charter',
        
        # Configurações
        'operational_costs_params': 'Parâmetros de Custos Operacionais',
        'market_reference_prices': 'Preços de Referência do Mercado',
        'formulas_used': 'Fórmulas Utilizadas',
        'current_parameters': 'Parâmetros Atuais',
        'impact_preview': 'Preview do Impacto',
        
        # Parâmetros Específicos
        'fuel_price': 'Preço do Combustível (R$/L)',
        'pilot_cost_hour': 'Custo Piloto (R$/h)',
        'annual_depreciation': 'Depreciação Anual (%)',
        'maintenance_costs': 'Custos de Manutenção',
        'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
        'maintenance_jet': 'Manutenção Jato (R$/h)',
        'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
        'market_price_jet': 'Preço Mercado Jato (R$/h)',
        
        # Status e Informações
        'system_status': 'Status do Sistema',
        'system_operational': 'Sistema Operacional',
        'models_configured': 'modelos configurados',
        'parameters_loaded': 'Parâmetros carregados',
        'features': 'Funcionalidades',
        'usage_tips': 'Dicas de Uso',
        'quick_actions': 'Ações Rápidas',
        
        # Mensagens de Sucesso/Erro
        'calculation_success': 'Cálculo realizado com sucesso',
        'settings_saved': 'Configurações salvas com sucesso!',
        'settings_save_error': 'Erro ao salvar configurações',
        'calculation_error': 'Erro no cálculo',
        'data_load_error': 'Erro ao carregar dados',
        'no_models_configured': 'Nenhum modelo configurado',
        'parameters_validation_error': 'Erro na validação dos parâmetros',
        
        # Insights e Análises
        'profitable_operation': 'Operação Rentável',
        'operation_at_loss': 'Atenção: Operação no Prejuízo',
        'monthly_deficit': 'Déficit mensal',
        'recommend_increase_occupancy': 'Recomenda-se aumentar ocupação ou revisar custos',
        'excellent_viability': 'Excelente viabilidade econômica',
        'consider_increase_frequency': 'Considere aumentar a frequência nesta operação',
        
        # Gráficos e Visualizações
        'financial_breakdown_monthly': 'Breakdown Financeiro Mensal',
        'annual_cost_comparison': 'Comparativo Anual: Gestão Própria vs. Amaro Aviation',
        'cost_composition': 'Composição de Custos',
        'annual_savings_chart': 'Economia Anual',
        
        # Tooltips e Ajuda
        'occupancy_tooltip': 'Percentual de utilização efetiva da aeronave',
        'fixed_costs_tooltip': 'Hangar, seguro, financiamento, etc.',
        'charter_revenue_tooltip': 'Considerar receita compensatória do charter',
        'realistic_projections_tip': 'Use ocupação de 70-80% para projeções realistas',
        'consider_real_fixed_costs': 'Considere custos fixos reais (hangar, seguro, etc.)',
        'review_parameters_periodically': 'Revise parâmetros periodicamente',
        'export_presentations': 'Exporte relatórios para apresentações',
        
        # Fórmulas
        'cost_calculation_formula': 'Cálculo de Custo por Hora',
        'savings_calculation_formula': 'Cálculo de Economia',
        'roi_calculation_formula': 'Cálculo de ROI',
        'formula_where': 'Onde:',
        'formula_fuel': 'Combustível = Consumo (L/h) × Preço Combustível (R$/L)',
        'formula_pilot': 'Piloto = Custo Piloto (R$/h)',
        'formula_maintenance': 'Manutenção = Custo Manutenção por tipo (R$/h)',
        'formula_depreciation': 'Depreciação = (Valor Aeronave × % Depreciação Anual) ÷ Horas Anuais',
        
        # Footer
        'developed_with_love': 'Desenvolvido com ❤️ para excelência comercial',
        'refactored_system': 'Sistema Refatorado',
        'version': 'v3.0'
    },
    
    # English (US)
    'en': {
        # Main Interface
        'app_title': 'Amaro Aviation',
        'app_subtitle': 'Smart Operating Cost Calculator',
        'language_selector': '🌐 Language',
        
        # Navigation and Tabs
        'tab_monthly_profit': '📈 Monthly Profit Estimation',
        'tab_cost_comparison': '⚖️ Cost Comparison',
        'tab_settings': '⚙️ Settings & Formulas',
        
        # Input Fields
        'aircraft_model': 'Aircraft Model',
        'flight_hours_month': 'Flight Hours per Month',
        'occupancy_rate': 'Occupancy Rate (%)',
        'annual_hours': 'Annual Flight Hours',
        'fixed_costs_annual': 'Annual Fixed Costs (R$)',
        'include_charter_revenue': 'Include Charter Revenue',
        
        # Buttons
        'calculate': '🚀 Calculate',
        'save_settings': '💾 Save Settings',
        'reload_data': '🔄 Reload Data',
        'presentation_mode': '📱 Presentation Mode',
        'export_excel': '📊 Download Excel Report',
        'export_pdf': '📄 Download PDF Report',
        'export_text': '📄 Download Text Report',
        
        # Results - Monthly Profit
        'gross_revenue': 'Gross Revenue',
        'owner_share': 'Owner Revenue',
        'amaro_share': 'Amaro Aviation Fee',
        'operational_costs': 'Operational Costs',
        'net_profit': 'Net Profit',
        'monthly_roi': 'Monthly ROI',
        'projected_annual_revenue': 'Projected Annual Revenue',
        
        # Results - Comparison
        'own_management': 'Own Management',
        'amaro_management': 'Amaro Aviation Management',
        'annual_savings': 'Annual Savings',
        'monthly_savings': 'Monthly Savings',
        'savings_percentage': 'Savings Percentage',
        'fixed_costs': 'Fixed Costs',
        'variable_costs': 'Variable Costs',
        'charter_revenue': 'Charter Revenue',
        
        # Settings
        'operational_costs_params': 'Operational Cost Parameters',
        'market_reference_prices': 'Market Reference Prices',
        'formulas_used': 'Formulas Used',
        'current_parameters': 'Current Parameters',
        'impact_preview': 'Impact Preview',
        
        # Specific Parameters
        'fuel_price': 'Fuel Price (R$/L)',
        'pilot_cost_hour': 'Pilot Cost (R$/h)',
        'annual_depreciation': 'Annual Depreciation (%)',
        'maintenance_costs': 'Maintenance Costs',
        'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
        'maintenance_jet': 'Jet Maintenance (R$/h)',
        'market_price_turboprop': 'Turboprop Market Price (R$/h)',
        'market_price_jet': 'Jet Market Price (R$/h)',
        
        # Status and Information
        'system_status': 'System Status',
        'system_operational': 'System Operational',
        'models_configured': 'models configured',
        'parameters_loaded': 'Parameters loaded',
        'features': 'Features',
        'usage_tips': 'Usage Tips',
        'quick_actions': 'Quick Actions',
        
        # Success/Error Messages
        'calculation_success': 'Calculation completed successfully',
        'settings_saved': 'Settings saved successfully!',
        'settings_save_error': 'Error saving settings',
        'calculation_error': 'Calculation error',
        'data_load_error': 'Error loading data',
        'no_models_configured': 'No models configured',
        'parameters_validation_error': 'Parameter validation error',
        
        # Insights and Analysis
        'profitable_operation': 'Profitable Operation',
        'operation_at_loss': 'Warning: Operation at Loss',
        'monthly_deficit': 'Monthly deficit',
        'recommend_increase_occupancy': 'Recommend increasing occupancy or reviewing costs',
        'excellent_viability': 'Excellent economic viability',
        'consider_increase_frequency': 'Consider increasing frequency for this operation',
        
        # Charts and Visualizations
        'financial_breakdown_monthly': 'Monthly Financial Breakdown',
        'annual_cost_comparison': 'Annual Comparison: Own Management vs. Amaro Aviation',
        'cost_composition': 'Cost Composition',
        'annual_savings_chart': 'Annual Savings',
        
        # Tooltips and Help
        'occupancy_tooltip': 'Effective utilization percentage of the aircraft',
        'fixed_costs_tooltip': 'Hangar, insurance, financing, etc.',
        'charter_revenue_tooltip': 'Consider compensatory charter revenue',
        'realistic_projections_tip': 'Use 70-80% occupancy for realistic projections',
        'consider_real_fixed_costs': 'Consider real fixed costs (hangar, insurance, etc.)',
        'review_parameters_periodically': 'Review parameters periodically',
        'export_presentations': 'Export reports for presentations',
        
        # Formulas
        'cost_calculation_formula': 'Cost per Hour Calculation',
        'savings_calculation_formula': 'Savings Calculation',
        'roi_calculation_formula': 'ROI Calculation',
        'formula_where': 'Where:',
        'formula_fuel': 'Fuel = Consumption (L/h) × Fuel Price (R$/L)',
        'formula_pilot': 'Pilot = Pilot Cost (R$/h)',
        'formula_maintenance': 'Maintenance = Maintenance Cost per type (R$/h)',
        'formula_depreciation': 'Depreciation = (Aircraft Value × Annual Depreciation %) ÷ Annual Hours',
        
        # Footer
        'developed_with_love': 'Developed with ❤️ for commercial excellence',
        'refactored_system': 'Refactored System',
        'version': 'v3.0'
    }
}

def get_text(key, lang='pt'):
    """
    Obtém texto traduzido baseado na chave e idioma
    
    Args:
        key: Chave da tradução
        lang: Código do idioma ('pt' ou 'en')
    
    Returns:
        String traduzida ou a própria chave se não encontrada
    """
    try:
        return TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)
    except Exception:
        return key

def get_available_languages():
    """
    Retorna lista de idiomas disponíveis
    
    Returns:
        List: Lista de códigos de idioma disponíveis
    """
    return list(TRANSLATIONS.keys())

def get_language_options():
    """
    Retorna opções de idioma formatadas para selectbox
    
    Returns:
        List: Lista de opções formatadas
    """
    return [
        "🇧🇷 Português",
        "🇺🇸 English"
    ]

def detect_language_from_selection(selection):
    """
    Detecta código do idioma a partir da seleção do usuário
    
    Args:
        selection: String selecionada pelo usuário
    
    Returns:
        String: Código do idioma ('pt' ou 'en')
    """
    if '🇧🇷' in selection:
        return 'pt'
    elif '🇺🇸' in selection:
        return 'en'
    else:
        return 'pt'  # Default para português

def translate_dict(data_dict, lang='pt', prefix=''):
    """
    Traduz chaves de um dicionário usando as traduções disponíveis
    
    Args:
        data_dict: Dicionário para traduzir
        lang: Idioma alvo
        prefix: Prefixo para as chaves de tradução
    
    Returns:
        Dict: Dicionário com chaves traduzidas
    """
    translated = {}
    
    for key, value in data_dict.items():
        # Tentar encontrar tradução
        translation_key = f"{prefix}_{key}" if prefix else key
        translated_key = get_text(translation_key, lang)
        
        # Se não encontrou tradução, usar chave original formatada
        if translated_key == translation_key:
            translated_key = key.replace('_', ' ').title()
        
        translated[translated_key] = value
    
    return translated

def format_currency(value, lang='pt'):
    """
    Formata valores monetários de acordo com o idioma
    
    Args:
        value: Valor numérico
        lang: Idioma para formatação
    
    Returns:
        String: Valor formatado
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
        lang: Idioma para formatação
    
    Returns:
        String: Percentual formatado
    """
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except Exception:
        return str(value)

def get_month_names(lang='pt'):
    """
    Retorna nomes dos meses no idioma especificado
    
    Args:
        lang: Código do idioma
    
    Returns:
        List: Lista com nomes dos meses
    """
    if lang == 'pt':
        return [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
    else:
        return [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

def get_aircraft_types(lang='pt'):
    """
    Retorna tipos de aeronave traduzidos
    
    Args:
        lang: Código do idioma
    
    Returns:
        Dict: Dicionário com tipos traduzidos
    """
    if lang == 'pt':
        return {
            'turboprop': 'Turboprop',
            'jato': 'Jato',
            'jet': 'Jato'
        }
    else:
        return {
            'turboprop': 'Turboprop',
            'jato': 'Jet',
            'jet': 'Jet'
        }

# Classe auxiliar para gerenciamento de idioma
class LanguageManager:
    """
    Classe para gerenciar idioma da aplicação de forma centralizada
    """
    
    def __init__(self, default_lang='pt'):
        self.current_lang = default_lang
    
    def set_language(self, lang):
        """Define idioma atual"""
        if lang in get_available_languages():
            self.current_lang = lang
    
    def get_current_language(self):
        """Retorna idioma atual"""
        return self.current_lang
    
    def t(self, key):
        """Método de conveniência para tradução"""
        return get_text(key, self.current_lang)
    
    def format_currency(self, value):
        """Método de conveniência para formatação monetária"""
        return format_currency(value, self.current_lang)
    
    def format_percentage(self, value):
        """Método de conveniência para formatação percentual"""
        return format_percentage(value, self.current_lang)

# Instância global para uso em toda aplicação
language_manager = LanguageManager()

# Funções de conveniência para compatibilidade
def t(key, lang='pt'):
    """Função de conveniência para tradução"""
    return get_text(key, lang)

def set_language(lang):
    """Define idioma globalmente"""
    language_manager.set_language(lang)

def get_current_language():
    """Obtém idioma atual"""
    return language_manager.get_current_language()

# Exemplo de uso
if __name__ == "__main__":
    # Testes básicos
    print("=== Teste do Sistema de Idiomas ===")
    print()
    
    # Teste em português
    print("Português:")
    print(f"Título: {get_text('app_title', 'pt')}")
    print(f"Subtítulo: {get_text('app_subtitle', 'pt')}")
    print(f"Botão Calcular: {get_text('calculate', 'pt')}")
    print()
    
    # Teste em inglês
    print("English:")
    print(f"Title: {get_text('app_title', 'en')}")
    print(f"Subtitle: {get_text('app_subtitle', 'en')}")
    print(f"Calculate Button: {get_text('calculate', 'en')}")
    print()
    
    # Teste de formatação
    print("Formatação:")
    valor = 1234567.89
    print(f"Português: {format_currency(valor, 'pt')}")
    print(f"English: {format_currency(valor, 'en')}")
    print()
    
    # Teste LanguageManager
    print("LanguageManager:")
    lm = LanguageManager('en')
    print(f"Current language: {lm.get_current_language()}")
    print(f"App title: {lm.t('app_title')}")
    print(f"Formatted currency: {lm.format_currency(1500.50)}")
    
    print("\n✅ Testes concluídos com sucesso!")