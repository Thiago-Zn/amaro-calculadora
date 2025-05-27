"""
Sistema de idiomas para aplicação multipage
Compatível com a estrutura de páginas do Streamlit
"""

def get_translations():
    """Traduções organizadas para estrutura multipage"""
    return {
        'pt': {
            # Interface Principal
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Simulador Estratégico de Custos',
            'language': 'Idioma / Language',
            'welcome_message': 'Bem-vindo ao simulador de custos operacionais mais completo do mercado',
            
            # Páginas
            'page_profit': 'Estimativa de Lucro',
            'page_breakdown': 'Breakdown de Custos',
            'page_simulator': 'Simulador de Rotas',
            'page_projection': 'Projeção e Breakeven',
            'page_settings': 'Configurações',
            
            # Campos comuns
            'aircraft_model': 'Modelo da Aeronave',
            'flight_hours': 'Horas de Voo',
            'calculate': 'Calcular',
            'export': 'Exportar',
            'save': 'Salvar',
            'cancel': 'Cancelar',
            
            # Estimativa de Lucro
            'monthly_hours': 'Horas de Charter/mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'charter_price': 'Preço Hora Charter (R$)',
            'gross_revenue': 'Receita Bruta Mensal',
            'owner_revenue': 'Receita do Proprietário (90%)',
            'net_profit': 'Lucro Líquido',
            'monthly_roi': 'ROI Mensal',
            'revenue_composition': 'Composição de Receitas',
            'cost_breakdown': 'Breakdown de Custos Operacionais',
            'profitable_operation': 'Operação Lucrativa',
            'operation_deficit': 'Operação com Déficit',
            
            # Breakdown de Custos
            'annual_hours': 'Horas de Voo Anuais',
            'include_charter': 'Incluir Receita de Charter na Comparação',
            'fixed_costs': 'Custos Fixos Anuais (Gestão Própria)',
            'hangar_cost': 'Hangaragem (R$/ano)',
            'insurance_cost': 'Seguro (R$/ano)',
            'crew_cost': 'Tripulação Fixa (R$/ano)',
            'admin_cost': 'Administração (R$/ano)',
            'own_management': 'Custo Total - Gestão Própria',
            'amaro_management': 'Custo Total - Gestão Amaro',
            'annual_savings': 'Economia Anual',
            'cost_reduction': 'de redução de custos',
            'detailed_breakdown': 'Breakdown Detalhado de Custos',
            'hangar': 'Hangaragem',
            'insurance': 'Seguro Aeronáutico',
            'crew': 'Tripulação Dedicada',
            'administration': 'Administração/Planejamento',
            'fuel': 'Combustível',
            'maintenance': 'Manutenção',
            'depreciation': 'Depreciação',
            'other_costs': 'Outros Custos Variáveis',
            'charter_revenue': 'Receita Charter (compensação)',
            'net_total': 'TOTAL LÍQUIDO',
            'cost_distribution': 'Distribuição de Custos - Gestão Própria',
            'fixed_costs_label': 'Custos Fixos',
            'variable_costs_label': 'Custos Variáveis',
            'accumulated_savings': 'Economia Acumulada em 5 Anos',
            
            # Simulador de Rotas
            'origin_airport': 'Aeroporto de Origem',
            'destination_airport': 'Aeroporto de Destino',
            'simulate_route': 'Simular Rota',
            'route_analysis': 'Análise da Rota',
            'flight_duration': 'Duração do Voo',
            'total_cost_amaro': 'Custo Total Amaro',
            'market_price': 'Preço de Mercado',
            'savings': 'Economia',
            'cost_composition': 'Composição de Custos',
            'visual_comparison': 'Comparativo Visual',
            'amaro_cost': 'Custo Amaro',
            'market_price_label': 'Preço Mercado',
            'advantageous_route': 'Rota Vantajosa',
            'route_attention': 'Atenção',
            'amaro_savings_message': 'A gestão Amaro oferece economia de',
            'cost_above_market': 'O custo operacional está acima do preço de mercado',
            'consider_optimizations': 'Considere otimizações operacionais para esta rota',
            
            # Projeção de Longo Prazo
            'projection_horizon': 'Horizonte de Projeção (meses)',
            'growth_rate': 'Crescimento Anual (%)',
            'advanced_parameters': 'Parâmetros Avançados',
            'initial_investment': 'Investimento Inicial (R$)',
            'occupancy_charter': 'Taxa de Ocupação Charter (%)',
            'cost_inflation': 'Inflação de Custos (%/ano)',
            'charter_adjustment': 'Reajuste Preço Charter (%/ano)',
            'generate_projection': 'Gerar Projeção',
            'projection_analysis': 'Análise de Projeção',
            'total_revenue_projected': 'Receita Total Projetada',
            'total_cost_projected': 'Custo Total Projetado',
            'total_profit_projected': 'Lucro Total Projetado',
            'breakeven': 'Breakeven',
            'return_investment': 'Retorno do investimento',
            'outside_horizon': 'Fora do horizonte',
            'long_term_projection': 'Projeção Financeira de Longo Prazo',
            'months': 'Meses',
            'value_currency': 'Valor (R$)',
            'accumulated_revenue': 'Receita Acumulada',
            'accumulated_cost': 'Custo Acumulado',
            'cash_flow': 'Fluxo de Caixa',
            'important_milestones': 'Marcos Importantes da Projeção',
            'milestone': 'Marco',
            'accumulated_profit': 'Lucro Acumulado',
            
            # Configurações
            'financial_parameters': 'Parâmetros Financeiros',
            'aircraft_models': 'Modelos de Aeronaves',
            'available_routes': 'Rotas Disponíveis',
            'operational_costs': 'Custos Operacionais',
            'fuel_price': 'Preço do Combustível (R$/litro)',
            'pilot_cost': 'Custo Hora Piloto (R$)',
            'annual_depreciation': 'Depreciação Anual (%)',
            'maintenance_by_type': 'Custos de Manutenção por Tipo',
            'turboprop_maintenance': 'Manutenção Turboprop (R$/hora)',
            'jet_maintenance': 'Manutenção Jato (R$/hora)',
            'market_prices': 'Preços de Mercado (Charter)',
            'turboprop_charter': 'Preço Charter Turboprop (R$/hora)',
            'jet_charter': 'Preço Charter Jato (R$/hora)',
            'save_financial_config': 'Salvar Configurações Financeiras',
            'aircraft_management': 'Gerenciamento de Modelos de Aeronaves',
            'edit_existing_models': 'Editar Modelos Existentes',
            'model': 'Modelo',
            'consumption': 'Consumo (L/h)',
            'maintenance_type': 'Tipo Manutenção',
            'aircraft_type': 'Tipo Aeronave',
            'save_model_changes': 'Salvar Alterações nos Modelos',
            'download_template': 'Baixar Template CSV',
            'route_management': 'Gerenciamento de Rotas',
            'edit_available_routes': 'Editar Rotas Disponíveis',
            'origin': 'Origem',
            'destination': 'Destino',
            'duration': 'Duração (h)',
            'save_route_changes': 'Salvar Alterações nas Rotas',
            'config_saved': 'Configurações salvas com sucesso!',
            'models_updated': 'Modelos atualizados com sucesso!',
            'routes_updated': 'Rotas atualizadas com sucesso!',
            'save_error': 'Erro ao salvar',
            
            # Status e mensagens
            'system_not_configured': 'Sistema não configurado. Execute o setup inicial.',
            'system_load_error': 'Erro ao carregar sistema',
            'routes_not_found': 'Arquivo de rotas não encontrado. Usando rotas padrão.',
            'no_models_configured': 'Nenhum modelo configurado',
        },
        'en': {
            # Main Interface
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Strategic Cost Simulator',
            'language': 'Language / Idioma',
            'welcome_message': 'Welcome to the most complete operational cost simulator in the market',
            
            # Pages
            'page_profit': 'Profit Estimation',
            'page_breakdown': 'Cost Breakdown',
            'page_simulator': 'Route Simulator',
            'page_projection': 'Projection and Breakeven',
            'page_settings': 'Settings',
            
            # Common fields
            'aircraft_model': 'Aircraft Model',
            'flight_hours': 'Flight Hours',
            'calculate': 'Calculate',
            'export': 'Export',
            'save': 'Save',
            'cancel': 'Cancel',
            
            # Profit Estimation
            'monthly_hours': 'Charter Hours/month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'charter_price': 'Charter Hour Price (R$)',
            'gross_revenue': 'Monthly Gross Revenue',
            'owner_revenue': 'Owner Revenue (90%)',
            'net_profit': 'Net Profit',
            'monthly_roi': 'Monthly ROI',
            'revenue_composition': 'Revenue Composition',
            'cost_breakdown': 'Operational Cost Breakdown',
            'profitable_operation': 'Profitable Operation',
            'operation_deficit': 'Operation with Deficit',
            
            # Cost Breakdown
            'annual_hours': 'Annual Flight Hours',
            'include_charter': 'Include Charter Revenue in Comparison',
            'fixed_costs': 'Annual Fixed Costs (Own Management)',
            'hangar_cost': 'Hangar (R$/year)',
            'insurance_cost': 'Insurance (R$/year)',
            'crew_cost': 'Fixed Crew (R$/year)',
            'admin_cost': 'Administration (R$/year)',
            'own_management': 'Total Cost - Own Management',
            'amaro_management': 'Total Cost - Amaro Management',
            'annual_savings': 'Annual Savings',
            'cost_reduction': 'cost reduction',
            'detailed_breakdown': 'Detailed Cost Breakdown',
            'hangar': 'Hangar',
            'insurance': 'Aeronautical Insurance',
            'crew': 'Dedicated Crew',
            'administration': 'Administration/Planning',
            'fuel': 'Fuel',
            'maintenance': 'Maintenance',
            'depreciation': 'Depreciation',
            'other_costs': 'Other Variable Costs',
            'charter_revenue': 'Charter Revenue (offset)',
            'net_total': 'NET TOTAL',
            'cost_distribution': 'Cost Distribution - Own Management',
            'fixed_costs_label': 'Fixed Costs',
            'variable_costs_label': 'Variable Costs',
            'accumulated_savings': '5-Year Accumulated Savings',
            
            # Route Simulator
            'origin_airport': 'Origin Airport',
            'destination_airport': 'Destination Airport',
            'simulate_route': 'Simulate Route',
            'route_analysis': 'Route Analysis',
            'flight_duration': 'Flight Duration',
            'total_cost_amaro': 'Total Amaro Cost',
            'market_price': 'Market Price',
            'savings': 'Savings',
            'cost_composition': 'Cost Composition',
            'visual_comparison': 'Visual Comparison',
            'amaro_cost': 'Amaro Cost',
            'market_price_label': 'Market Price',
            'advantageous_route': 'Advantageous Route',
            'route_attention': 'Attention',
            'amaro_savings_message': 'Amaro management offers savings of',
            'cost_above_market': 'Operating cost is above market price',
            'consider_optimizations': 'Consider operational optimizations for this route',
            
            # Long-term Projection
            'projection_horizon': 'Projection Horizon (months)',
            'growth_rate': 'Annual Growth (%)',
            'advanced_parameters': 'Advanced Parameters',
            'initial_investment': 'Initial Investment (R$)',
            'occupancy_charter': 'Charter Occupancy Rate (%)',
            'cost_inflation': 'Cost Inflation (%/year)',
            'charter_adjustment': 'Charter Price Adjustment (%/year)',
            'generate_projection': 'Generate Projection',
            'projection_analysis': 'Projection Analysis',
            'total_revenue_projected': 'Total Projected Revenue',
            'total_cost_projected': 'Total Projected Cost',
            'total_profit_projected': 'Total Projected Profit',
            'breakeven': 'Breakeven',
            'return_investment': 'Return on investment',
            'outside_horizon': 'Outside horizon',
            'long_term_projection': 'Long-term Financial Projection',
            'months': 'Months',
            'value_currency': 'Value (R$)',
            'accumulated_revenue': 'Accumulated Revenue',
            'accumulated_cost': 'Accumulated Cost',
            'cash_flow': 'Cash Flow',
            'important_milestones': 'Important Projection Milestones',
            'milestone': 'Milestone',
            'accumulated_profit': 'Accumulated Profit',
            
            # Settings
            'financial_parameters': 'Financial Parameters',
            'aircraft_models': 'Aircraft Models',
            'available_routes': 'Available Routes',
            'operational_costs': 'Operational Costs',
            'fuel_price': 'Fuel Price (R$/liter)',
            'pilot_cost': 'Pilot Hour Cost (R$)',
            'annual_depreciation': 'Annual Depreciation (%)',
            'maintenance_by_type': 'Maintenance Costs by Type',
            'turboprop_maintenance': 'Turboprop Maintenance (R$/hour)',
            'jet_maintenance': 'Jet Maintenance (R$/hour)',
            'market_prices': 'Market Prices (Charter)',
            'turboprop_charter': 'Turboprop Charter Price (R$/hour)',
            'jet_charter': 'Jet Charter Price (R$/hour)',
            'save_financial_config': 'Save Financial Settings',
            'aircraft_management': 'Aircraft Model Management',
            'edit_existing_models': 'Edit Existing Models',
            'model': 'Model',
            'consumption': 'Consumption (L/h)',
            'maintenance_type': 'Maintenance Type',
            'aircraft_type': 'Aircraft Type',
            'save_model_changes': 'Save Model Changes',
            'download_template': 'Download CSV Template',
            'route_management': 'Route Management',
            'edit_available_routes': 'Edit Available Routes',
            'origin': 'Origin',
            'destination': 'Destination',
            'duration': 'Duration (h)',
            'save_route_changes': 'Save Route Changes',
            'config_saved': 'Settings saved successfully!',
            'models_updated': 'Models updated successfully!',
            'routes_updated': 'Routes updated successfully!',
            'save_error': 'Error saving',
            
            # Status and messages
            'system_not_configured': 'System not configured. Run initial setup.',
            'system_load_error': 'Error loading system',
            'routes_not_found': 'Routes file not found. Using default routes.',
            'no_models_configured': 'No models configured',
        }
    }

def get_text(key, lang='pt'):
    """
    Obtém texto traduzido com fallback
    
    Args:
        key: Chave da tradução
        lang: Código do idioma ('pt' ou 'en')
    
    Returns:
        String traduzida ou chave se não encontrada
    """
    try:
        translations = get_translations()
        return translations.get(lang, translations['pt']).get(key, key)
    except:
        return key

def t(key, lang='pt'):
    """Função de conveniência para tradução"""
    return get_text(key, lang)

def detect_language_from_selection(selection):
    """
    Detecta idioma baseado na seleção do selectbox
    
    Args:
        selection: String selecionada ("🇧🇷 Português" ou "🇺🇸 English")
    
    Returns:
        String: 'pt' ou 'en'
    """
    return 'pt' if '🇧🇷' in selection else 'en'