import streamlit as st

def apply_amaro_theme():
    """
    Aplica um tema CSS customizado para a Amaro Aviation em uma aplicação Streamlit.
    Este tema estiliza a sidebar, header, botões, tabs e cards.
    """
    custom_css = """
    <style>
        /* === Cores Base Amaro Aviation === */
        :root {
            --amaro-bordo: #8C1D40;
            --amaro-bordo-escuro: #A02050; /* Para hover/ativo */
            --amaro-bordo-mais-escuro: #731734; /* Para clique de botão */
            --amaro-branco: #FFFFFF;
            --amaro-cinza-texto: #31333F; /* Cinza escuro padrão Streamlit para texto */
            --amaro-cinza-claro-fundo: #F0F2F6; /* Cinza claro para fundos sutis */
            --amaro-cinza-borda: #D3D3D3; /* Cinza para bordas */
        }

        /* === Sidebar === */
        [data-testid="stSidebar"] {
            background-color: var(--amaro-bordo);
        }

        /* Texto geral na sidebar (títulos de widgets, labels) */
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb, /* Títulos de seção (pode variar) */
        [data-testid="stSidebar"] .st-emotion-cache-q8sbsg, /* Labels de widgets (pode variar) */
        [data-testid="stSidebar"] .st-emotion-cache-1gulkj5, /* Outros textos (pode variar) */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6 {
            color: var(--amaro-branco) !important;
        }

        /* Itens de navegação na sidebar (links de página) */
        [data-testid="stSidebar"] [data-testid="stPageLink"],
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a { /* Para versões mais antigas de st.navigation */
            color: var(--amaro-branco);
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
            border-radius: 0.25rem; /* Leve arredondamento */
            margin: 0.1rem 0.5rem; /* Espaçamento */
            padding: 0.5rem 0.8rem; /* Padding interno */
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] p,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a p {
            color: var(--amaro-branco) !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] svg,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a svg {
            fill: var(--amaro-branco) !important;
        }

        /* Item de navegação ATIVO na sidebar */
        [data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"],
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a[aria-current="page"] {
            background-color: var(--amaro-bordo-escuro);
            color: var(--amaro-branco) !important;
            font-weight: bold;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] p,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a[aria-current="page"] p {
             color: var(--amaro-branco) !important;
             font-weight: bold;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"][aria-current="page"] svg,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a[aria-current="page"] svg {
            fill: var(--amaro-branco) !important;
        }

        /* Item de navegação HOVER na sidebar */
        [data-testid="stSidebar"] [data-testid="stPageLink"]:hover,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a:hover {
            background-color: var(--amaro-bordo-escuro);
            color: var(--amaro-branco) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25); /* Sombra sutil */
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"]:hover p,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a:hover p {
             color: var(--amaro-branco) !important;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"]:hover svg,
        [data-testid="stSidebar"] [data-testid="stMainNav"] ul li a:hover svg {
            fill: var(--amaro-branco) !important;
        }

        /* === Header Principal === */
        [data-testid="stHeader"] {
            background-image: linear-gradient(to right, var(--amaro-bordo), var(--amaro-bordo-escuro));
            color: var(--amaro-branco); /* Texto branco, se houver texto direto no header */
        }
        /* Título da aplicação no header (se existir e for padrão) */
        [data-testid="stHeader"] h1, [data-testid="stHeader"] h2, [data-testid="stHeader"] h3 {
            color: var(--amaro-branco);
        }

        /* === Botões === */
        .stButton>button {
            background-color: var(--amaro-bordo);
            color: var(--amaro-branco);
            border: 1px solid var(--amaro-bordo);
            border-radius: 0.25rem;
            padding: 0.4rem 0.8rem; /* Ajuste de padding */
            transition: background-color 0.2s ease, border-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: var(--amaro-bordo-escuro);
            border-color: var(--amaro-bordo-escuro);
            color: var(--amaro-branco);
        }
        .stButton>button:focus { /* Mantém o foco visível e consistente */
            box-shadow: 0 0 0 0.2rem rgba(140, 29, 64, 0.4); 
            outline: none;
        }
        .stButton>button:active {
            background-color: var(--amaro-bordo-mais-escuro);
            border-color: var(--amaro-bordo-mais-escuro);
        }

        /* === Tabs === */
        .stTabs [role="tablist"] {
            border-bottom: 2px solid var(--amaro-cinza-borda);
            padding-bottom: 0; /* Remove padding extra se houver */
        }
        .stTabs [data-baseweb="tab"] {
            background-color: var(--amaro-branco);
            color: var(--amaro-cinza-texto);
            border: 1px solid transparent;
            border-bottom: none; /* Evita dupla borda */
            padding: 0.6rem 1rem; /* Padding ajustado */
            transition: background-color 0.2s ease, color 0.2s ease;
            margin-right: 4px; /* Pequeno espaçamento entre tabs */
            border-top-left-radius: 0.25rem;
            border-top-right-radius: 0.25rem;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: var(--amaro-cinza-claro-fundo);
            color: var(--amaro-bordo);
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: var(--amaro-bordo);
            color: var(--amaro-branco);
            border-color: var(--amaro-bordo) var(--amaro-bordo) transparent var(--amaro-bordo);
            font-weight: bold;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"]:hover {
            background-color: var(--amaro-bordo-escuro);
            color: var(--amaro-branco);
        }

        /* === Cards (Estilo genérico para st.container ou divs com classe 'card-style') === */
        div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stMarkdownContainer"],
        div.stApp div[data-testid="stBlock"] div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stMarkdownContainer"], /* Seletor mais específico para evitar conflitos */
        .card-style { /* Adicione esta classe a containers ou markdown para estilo de card */
            background-color: var(--amaro-branco);
            border: 1px solid var(--amaro-cinza-borda);
            border-radius: 0.3rem; /* Raio de borda sutil */
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04); /* Sombra muito sutil */
            margin-bottom: 1rem;
        }
        .card-style p, .card-style h1, .card-style h2, .card-style h3, .card-style li {
            color: var(--amaro-cinza-texto); /* Garante que texto dentro do card seja escuro */
        }

        /* === Conteúdo Principal da Página === */
        /* Garante que o texto no corpo principal não herde a cor branca da sidebar */
        .main .block-container {
            color: var(--amaro-cinza-texto);
        }
        .main .block-container p,
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container li,
        .main .block-container span,
        .main .block-container div:not([data-testid="stSidebar"]) { /* Evita afetar a sidebar novamente */
            /* Não é ideal usar !important aqui, mas pode ser necessário se houver conflitos fortes */
            /* color: var(--amaro-cinza-texto); */
        }
        
        /* Ajuste para texto de markdown no corpo principal */
        .main .block-container div[data-testid="stMarkdownContainer"] p,
        .main .block-container div[data-testid="stMarkdownContainer"] h1,
        .main .block-container div[data-testid="stMarkdownContainer"] h2,
        .main .block-container div[data-testid="stMarkdownContainer"] h3,
        .main .block-container div[data-testid="stMarkdownContainer"] li {
            color: var(--amaro-cinza-texto) !important; /* Garante a cor correta */
        }


    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)