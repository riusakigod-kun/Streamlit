import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# ===================== CONFIGURACIÓN =====================
st.set_page_config(
    page_title="Dashboard Interactivo - EXOR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS PERSONALIZADO CON BOOTSTRAP =====================
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f8f9fa;
    }

    /* ============ COLORES PRINCIPALES ============ */
    :root {
        --primary: #ff8c00;
        --secondary: #1e40af;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --dark: #1f2937;
        --light: #f3f4f6;
    }

    /* ============ SIDEBAR STYLING ============ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2937 0%, #111827 100%) !important;
        padding: 0 !important;
    }

    /* ============ MAIN CONTENT ============ */
    .main {
        background: #f8f9fa !important;
    }

    /* ============ HEADER DASHBOARD ============ */
    .dashboard-header {
        background: white;
        padding: 25px 30px;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .dashboard-header h1 {
        color: #1f2937;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }

    .dashboard-header p {
        color: #6b7280;
        font-size: 14px;
        margin: 5px 0 0 0;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #dcfce7;
        color: #166534;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .status-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 22px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: var(--primary);
    }

    .metric-card.orange {
        border-top: 4px solid var(--primary);
    }

    .metric-card.blue {
        border-top: 4px solid var(--secondary);
    }

    .metric-card.green {
        border-top: 4px solid var(--success);
    }

    .metric-card.red {
        border-top: 4px solid var(--danger);
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .metric-label {
        font-size: 14px;
        color: #6b7280;
        margin: 8px 0 0 0;
        font-weight: 500;
    }

    /* ============ CHART CONTAINERS ============ */
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    .chart-card h3 {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 20px;
    }

    .chart-card p {
        font-size: 13px;
        color: #6b7280;
        margin: 0;
    }

    /* ============ TABLE STYLING ============ */
    .data-table {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .table {
        margin-bottom: 0;
    }

    .table thead {
        background: #f3f4f6;
        border-bottom: 2px solid #e5e7eb;
    }

    .table thead th {
        color: #374151;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 16px;
    }

    .table tbody td {
        padding: 16px;
        border-bottom: 1px solid #f3f4f6;
        color: #374151;
        font-size: 14px;
    }

    .table tbody tr:hover {
        background: #f9fafb;
    }

    /* ============ BADGES ============ */
    .badge-status {
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-success-custom {
        background: #dcfce7;
        color: #166534;
    }

    .badge-warning-custom {
        background: #fef3c7;
        color: #92400e;
    }

    .badge-danger-custom {
        background: #fee2e2;
        color: #991b1b;
    }

    .badge-info-custom {
        background: #dbeafe;
        color: #1e40af;
    }

    /* ============ BUTTONS ============ */
    .btn-primary-custom {
        background: var(--primary);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }

    .btn-primary-custom:hover {
        background: #e67e00;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,140,0,0.2);
    }

    /* ============ RESPONSIVE ============ */
    @media (max-width: 768px) {
        .dashboard-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 15px;
        }

        .metric-value {
            font-size: 24px;
        }

        .chart-card {
            padding: 16px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ===================== FUNCIONES AUXILIARES =====================

def detectar_tipo_columna(serie):
    """Detecta el tipo de dato de una columna"""
    if serie.dtype == 'object':
        try:
            pd.to_datetime(serie)
            return 'fecha'
        except (TypeError, ValueError):
            return 'categórica'
    elif pd.api.types.is_numeric_dtype(serie):
        return 'numérica'
    return 'otra'

def generar_graficos_automaticos(df, columnas_numericas, columnas_categoricas):
    """Genera gráficos basados en el tipo de dato"""
    graficos = []
    
    # Gráficos para columnas numéricas
    if len(columnas_numericas) > 0:
        for col in columnas_numericas[:4]:
            try:
                fig = px.histogram(
                    df,
                    x=col,
                    nbins=30,
                    title=f"📊 Distribución de {col}",
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(
                    template="plotly_white",
                    hovermode='x unified',
                    height=400
                )
                graficos.append(("numérica", col, fig))
            except Exception:
                pass
    
    # Gráficos para columnas categóricas
    if len(columnas_categoricas) > 0:
        for col in columnas_categoricas[:3]:
            try:
                valor_counts = df[col].value_counts().head(10)
                fig = px.bar(
                    x=valor_counts.index,
                    y=valor_counts.values,
                    title=f"📈 Conteo: {col}",
                    labels={'x': col, 'y': 'Cantidad'},
                    color_discrete_sequence=['#764ba2']
                )
                fig.update_layout(
                    template="plotly_white",
                    hovermode='x unified',
                    height=400,
                    showlegend=False
                )
                graficos.append(("categórica", col, fig))
            except Exception:
                pass
    
    return graficos

def calcular_estadisticas(df):
    """Calcula estadísticas principales"""
    stats = {
        'filas': len(df),
        'columnas': len(df.columns),
        'valores_nulos': df.isnull().sum().sum(),
        'columnas_numericas': df.select_dtypes(include=[np.number]).columns.tolist(),
        'columnas_categoricas': df.select_dtypes(include=['object']).columns.tolist()
    }
    return stats

# ===================== SIDEBAR PERSONALIZADO =====================

# Header del sidebar
with st.sidebar:
    st.markdown("""
        <div style="
            background: rgba(102, 126, 234, 0.1);
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        ">
            <div style="
                width: 45px;
                height: 45px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 20px;
            ">EX</div>
            <div>
                <h3 style="color: white; margin: 0; font-size: 16px;">EXOR</h3>
                <p style="color: #cbd5e0; margin: 2px 0 0 0; font-size: 12px;">Gestión de Flota</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Opción de navegación
    st.markdown("### 📁 Selecciona una opción")
    
    menu_principal = st.selectbox(
        "Navegación:",
        [
            "📊 Resumen General",
            "📦 Inventario Equipos",
            "👥 Conductores",
            "⚠️ Alertas",
            "📤 Cargar Datos"
        ],
        key="menu_principal"
    )
    
    st.markdown("---")
    st.markdown("### 📥 Cargar Datos")
    
    archivo = st.file_uploader(
        "Sube tu archivo Excel o CSV",
        type=["xlsx", "xls", "csv"],
        key="file_upload"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Opciones")
    
    mostrar_tabla = st.checkbox("Mostrar tabla de datos", value=True)
    mostrar_estadisticas = st.checkbox("Mostrar estadísticas", value=True)
    
    st.markdown("---")
    st.markdown("### 👤 Usuario")
    st.markdown("""
        <div style="
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        ">
            <div style="
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                margin: 0 auto 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            ">JM</div>
            <p style="color: white; margin: 0; font-weight: 600;">Jefe de Flota</p>
            <p style="color: #cbd5e0; margin: 4px 0 0 0; font-size: 12px;">EXORS A.C.</p>
        </div>
    """, unsafe_allow_html=True)

# ===================== CONTENIDO PRINCIPAL =====================

def mostrar_resumen():
    """Muestra el resumen general"""
    st.markdown("""
        <div class="dashboard-header">
            <div>
                <h1>📊 Panel General de Flota</h1>
                <p>Marzo 2025 · Resumen completo de operaciones</p>
            </div>
            <div class="status-badge">
                ● En vivo
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card orange">
                <p class="metric-value">3,308h</p>
                <p class="metric-label">AMARILLA TOTAL</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card blue">
                <p class="metric-value">6,306h</p>
                <p class="metric-label">BLANCA TOTAL</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card green">
                <p class="metric-value">184h</p>
                <p class="metric-label">PROM. EQUIPO</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card red">
                <p class="metric-value">226h</p>
                <p class="metric-label">MAX. REGISTRADA</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="chart-card">
                <h3>⏱️ Horas operativas por semana</h3>
                <p>Línea amarilla vs línea blanca · Marzo 2025</p>
            </div>
        """, unsafe_allow_html=True)
        
        data_horas = pd.DataFrame({
            'Semana': ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
            'Amarilla': [700, 750, 850, 800],
            'Blanca': [1050, 900, 1100, 1000]
        })
        
        fig = px.bar(
            data_horas,
            x='Semana',
            y=['Amarilla', 'Blanca'],
            title=None,
            color_discrete_map={'Amarilla': '#ff8c00', 'Blanca': '#1e40af'},
            barmode='group'
        )
        fig.update_layout(
            template="plotly_white",
            height=350,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(b=30, l=40, r=20, t=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div class="chart-card">
                <h3>📊 Distribución de flota</h3>
                <p>Por tipo de equipo</p>
            </div>
        """, unsafe_allow_html=True)
        
        data_flota = pd.DataFrame({
            'Tipo': ['Amarilla 35%', 'Camionetas 42%', 'Coasters 23%'],
            'Valor': [35, 42, 23]
        })
        
        fig = px.pie(
            data_flota,
            values='Valor',
            names='Tipo',
            color_discrete_sequence=['#ff8c00', '#1e40af', '#10b981'],
            hole=0.4
        )
        fig.update_layout(
            height=350,
            margin=dict(b=30, l=40, r=20, t=30)
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_inventario():
    """Muestra el inventario de equipos"""
    st.markdown("""
        <div class="dashboard-header">
            <div>
                <h1>📦 Inventario de Equipos</h1>
                <p>Gestión completa de la flota</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    data = {
        'ID': ['CM-001', 'CM-002', 'CM-003', 'CM-004', 'CM-005'],
        'Modelo': ['Excavadora CAT 320', 'Excavadora Komatsu PC210', 'Retroexcavadora JD 310L', 'Camión Volvo', 'Camión MAN'],
        'Empresa': ['Minería XYZ', 'Cerro Verde', 'Las Bambas', 'Minería XYZ', 'Cerro Verde'],
        'Estado': ['Activo', 'Activo', 'Mantenimiento', 'Activo', 'Inactivo'],
        'Responsable': ['Ing. Quispe R.', 'Ing. López M.', 'Ing. García H.', 'Ing. Quispe R.', 'Ing. López M.']
    }
    
    df_equipos = pd.DataFrame(data)
    
    with col1:
        filtro_estado = st.selectbox("Filtrar por Estado:", ['Todos'] + df_equipos['Estado'].unique().tolist(), key="inv_estado")
    
    with col2:
        filtro_empresa = st.selectbox("Filtrar por Empresa:", ['Todos'] + df_equipos['Empresa'].unique().tolist(), key="inv_empresa")
    
    if filtro_estado != 'Todos':
        df_equipos = df_equipos[df_equipos['Estado'] == filtro_estado]
    
    if filtro_empresa != 'Todos':
        df_equipos = df_equipos[df_equipos['Empresa'] == filtro_empresa]
    
    # Tabla profesional
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    html_table = f"""
    <table class="table">
        <thead>
            <tr>
                <th>ID Equipo</th>
                <th>Modelo</th>
                <th>Empresa</th>
                <th>Estado</th>
                <th>Responsable</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, row in df_equipos.iterrows():
        estado_badge = {
            'Activo': 'badge-success-custom',
            'Mantenimiento': 'badge-warning-custom',
            'Inactivo': 'badge-danger-custom'
        }.get(row['Estado'], 'badge-info-custom')
        
        html_table += f"""
        <tr>
            <td><strong>{row['ID']}</strong></td>
            <td>{row['Modelo']}</td>
            <td>{row['Empresa']}</td>
            <td><span class="badge-status {estado_badge}">{row['Estado']}</span></td>
            <td>{row['Responsable']}</td>
        </tr>
        """
    
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def mostrar_conductores():
    """Muestra información de conductores"""
    st.markdown("""
        <div class="dashboard-header">
            <div>
                <h1>👥 Gestión de Conductores</h1>
                <p>Personal autorizado para operar equipos</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card orange">
                <p class="metric-value">12</p>
                <p class="metric-label">TOTAL CONDUCTORES</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card green">
                <p class="metric-value">11</p>
                <p class="metric-label">LICENCIAS VIGENTES</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card red">
                <p class="metric-value">1</p>
                <p class="metric-label">POR VENCER</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card blue">
                <p class="metric-value">3</p>
                <p class="metric-label">CLIENTES</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    conductores = pd.DataFrame({
        'Nombre': ['Pedro Mamani', 'Félix Arce', 'Hugo Chura', 'Juan Flores', 'Carlos Mamani'],
        'Rol': ['Operador Senior', 'Operador', 'Operador', 'Operador', 'Operador'],
        'Licencia': ['Vigente', 'Vigente', 'Vigente', 'Vigente', 'Por Vencer'],
        'Equipos': [3, 2, 2, 2, 1]
    })
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    html_table = """
    <table class="table">
        <thead>
            <tr>
                <th>Nombre del Conductor</th>
                <th>Rol</th>
                <th>Estado Licencia</th>
                <th>Equipos Asignados</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, row in conductores.iterrows():
        estado_badge = 'badge-success-custom' if row['Licencia'] == 'Vigente' else 'badge-warning-custom'
        html_table += f"""
        <tr>
            <td><strong>{row['Nombre']}</strong></td>
            <td>{row['Rol']}</td>
            <td><span class="badge-status {estado_badge}">{row['Licencia']}</span></td>
            <td><strong>{row['Equipos']}</strong></td>
        </tr>
        """
    
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def mostrar_alertas():
    """Muestra alertas del sistema"""
    st.markdown("""
        <div class="dashboard-header">
            <div>
                <h1>⚠️ Alertas Críticas</h1>
                <p>Incidentes activos del sistema</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    alertas_df = pd.DataFrame({
        'Equipo': ['CM-007', 'CM-001', 'CM-004', 'CM-012', 'CM-019', 'CM-025', 'CM-031'],
        'Tipo': ['Mantenimiento', 'Horas Operación', 'Combustible', 'Neumáticos', 'Aceite', 'Batería', 'Revisión'],
        'Severidad': ['Crítico', 'Advertencia', 'Información', 'Advertencia', 'Información', 'Crítico', 'Advertencia']
    })
    
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    html_alerts = """
    <table class="table">
        <thead>
            <tr>
                <th>Equipo</th>
                <th>Tipo de Alerta</th>
                <th>Severidad</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, row in alertas_df.iterrows():
        badge_map = {
            'Crítico': 'badge-danger-custom',
            'Advertencia': 'badge-warning-custom',
            'Información': 'badge-info-custom'
        }
        badge_class = badge_map.get(row['Severidad'], 'badge-info-custom')
        
        html_alerts += f"""
        <tr>
            <td><strong>{row['Equipo']}</strong></td>
            <td>{row['Tipo']}</td>
            <td><span class="badge-status {badge_class}">{row['Severidad']}</span></td>
        </tr>
        """
    
    html_alerts += "</tbody></table>"
    st.markdown(html_alerts, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def mostrar_carga_datos():
    """Muestra la interfaz de carga de datos"""
    st.markdown("""
        <div class="dashboard-header">
            <div>
                <h1>📤 Cargar y Analizar Datos</h1>
                <p>Sube tu archivo Excel o CSV para análisis automático</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if archivo is not None:
        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)
            
            st.success(f"✅ Archivo cargado - {len(df)} filas detectadas")
            
            stats = calcular_estadisticas(df)
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card blue">
                        <p class="metric-value">{stats['filas']:,}</p>
                        <p class="metric-label">FILAS</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card orange">
                        <p class="metric-value">{stats['columnas']}</p>
                        <p class="metric-label">COLUMNAS</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                porcentaje_nulos = (stats['valores_nulos'] / (stats['filas'] * stats['columnas']) * 100) if (stats['filas'] * stats['columnas']) > 0 else 0
                st.markdown(f"""
                    <div class="metric-card red">
                        <p class="metric-value">{porcentaje_nulos:.1f}%</p>
                        <p class="metric-label">VALORES NULOS</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card green">
                        <p class="metric-value">{100 - porcentaje_nulos:.1f}%</p>
                        <p class="metric-label">CALIDAD</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="chart-card"><h3>📈 Análisis Visual Automático</h3></div>', unsafe_allow_html=True)
            
            graficos = generar_graficos_automaticos(
                df,
                stats['columnas_numericas'],
                stats['columnas_categoricas']
            )
            
            if graficos:
                col1, col2 = st.columns(2)
                for i, (tipo, columna, fig) in enumerate(graficos):
                    with (col1 if i % 2 == 0 else col2):
                        st.plotly_chart(fig, use_container_width=True)
            
            if mostrar_tabla:
                st.markdown('<div class="chart-card"><h3>📋 Vista de Datos</h3></div>', unsafe_allow_html=True)
                st.markdown('<div class="data-table">', unsafe_allow_html=True)
                st.dataframe(df.head(20), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception:
            st.error("❌ Error al procesar archivo")
            st.info("Verifica que el archivo esté en el formato correcto")
    else:
        st.markdown("""
            <div style="text-align: center; padding: 40px; background: white; border-radius: 12px; margin-top: 20px;">
                <h2 style="color: #ff8c00; margin-bottom: 15px;">📁 Selecciona un archivo</h2>
                <p style="color: #6b7280; margin-bottom: 20px;">Soporta Excel (.xlsx, .xls) y CSV</p>
                <div style="color: #6b7280; font-size: 14px;">
                    ✅ Análisis automático de datos<br>
                    ✅ Gráficos dinámicos<br>
                    ✅ Exportación de resultados
                </div>
            </div>
        """, unsafe_allow_html=True)

# ===================== ROUTER PRINCIPAL =====================

if menu_principal == "📊 Resumen General":
    mostrar_resumen()
elif menu_principal == "📦 Inventario Equipos":
    mostrar_inventario()
elif menu_principal == "👥 Conductores":
    mostrar_conductores()
elif menu_principal == "⚠️ Alertas":
    mostrar_alertas()
elif menu_principal == "📤 Cargar Datos":
    mostrar_carga_datos()

# CSS Personalizado con Tailwind
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2/dist/tailwind.min.css');
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .header-section {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    .data-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    h1 {
        color: #667eea !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 10px !important;
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-top: 30px !important;
        margin-bottom: 15px !important;
    }
    
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 10px;
    }
    
    [data-testid="stSidebarNav"] {
        color: white !important;
    }
    
    .sidebar-title {
        color: #667eea !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        margin-top: 20px !important;
    }
    
    </style>
""", unsafe_allow_html=True)