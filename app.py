import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from pathlib import Path

# ===================== CONFIGURACIÓN =====================
st.set_page_config(
    page_title="Dashboard Interactivo - EXOR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS PERSONALIZADO =====================
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ============ MAIN LAYOUT ============ */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a202c 0%, #0f1419 100%) !important;
        padding: 0 !important;
    }

    /* ============ SIDEBAR STYLING ============ */
    [data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
    }

    .sidebar-header {
        background: rgba(102, 126, 234, 0.1);
        padding: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .sidebar-logo {
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
    }

    .sidebar-title h2 {
        color: white;
        font-size: 16px;
        margin: 0;
    }

    .sidebar-title p {
        color: #cbd5e0;
        font-size: 12px;
        margin: 2px 0 0 0;
    }

    /* ============ MENU STYLING ============ */
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stButton {
        margin: 5px 0;
    }

    [data-testid="stSidebar"] button {
        width: 100%;
        padding: 12px 20px !important;
        text-align: left !important;
        color: #cbd5e0 !important;
        font-size: 14px !important;
        border: none !important;
        background: transparent !important;
        border-left: 3px solid transparent !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        color: white !important;
        border-left-color: #667eea !important;
        padding-left: 24px !important;
    }

    /* ============ MAIN CONTENT ============ */
    .content-header {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin: 40px 30px 30px 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .content-header h1 {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .content-header p {
        color: #718096;
        font-size: 1.1rem;
    }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }

    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }

    .data-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    }

    /* ============ BADGES ============ */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }

    .badge-danger {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
    }

    .badge-yellow {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #1a202c;
    }

    .badge-blue {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
    }

    /* ============ RESPONSIVE ============ */
    @media (max-width: 768px) {
        .content-header {
            margin: 20px !important;
            padding: 20px !important;
        }

        .content-header h1 {
            font-size: 1.5rem;
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
        except:
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
            except:
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
            except:
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
        <div class="content-header">
            <h1>📊 Resumen General</h1>
            <p>Visualiza el estado general de tu flota de equipos</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Equipos", "42", "Flota disponible")
    
    with col2:
        st.metric("✅ Equipos Activos", "35", "83.3%")
    
    with col3:
        st.metric("⚙️ En Mantenimiento", "5", "11.9%")
    
    with col4:
        st.metric("❌ Inactivos", "2", "4.8%")
    
    # Gráficos de ejemplo
    col1, col2 = st.columns(2)
    
    with col1:
        data_estado = pd.DataFrame({
            'Estado': ['Activo', 'Mantenimiento', 'Inactivo'],
            'Cantidad': [35, 5, 2]
        })
        fig = px.pie(
            data_estado,
            values='Cantidad',
            names='Estado',
            title='Distribución por Estado'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        data_linea = pd.DataFrame({
            'Línea': ['Amarilla', 'Blanca'],
            'Cantidad': [18, 24]
        })
        fig = px.bar(
            data_linea,
            x='Línea',
            y='Cantidad',
            title='Equipos por Línea'
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_inventario():
    """Muestra el inventario de equipos"""
    st.markdown("""
        <div class="content-header">
            <h1>📦 Inventario de Equipos</h1>
            <p>Ver todos los equipos registrados en el sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    data = {
        'ID': ['CM-001', 'CM-002', 'CM-003', 'CM-004', 'CM-005'],
        'Modelo': ['Excavadora CAT 320', 'Excavadora Komatsu PC210', 'Retroexcavadora JD 310L', 'Camión Volvo', 'Camión MAN'],
        'Empresa': ['Minería XYZ', 'Cerro Verde', 'Las Bambas', 'Minería XYZ', 'Cerro Verde'],
        'Estado': ['Activo', 'Activo', 'Mantenimiento', 'Activo', 'Inactivo'],
        'Responsable': ['Ing. Quispe R.', 'Ing. López M.', 'Ing. García H.', 'Ing. Quispe R.', 'Ing. López M.']
    }
    
    df_equipos = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    with col1:
        filtro_estado = st.selectbox("Filtrar por Estado:", ['Todos'] + df_equipos['Estado'].unique().tolist())
    
    with col2:
        filtro_empresa = st.selectbox("Filtrar por Empresa:", ['Todos'] + df_equipos['Empresa'].unique().tolist())
    
    if filtro_estado != 'Todos':
        df_equipos = df_equipos[df_equipos['Estado'] == filtro_estado]
    
    if filtro_empresa != 'Todos':
        df_equipos = df_equipos[df_equipos['Empresa'] == filtro_empresa]
    
    st.dataframe(df_equipos, use_container_width=True, hide_index=True)

def mostrar_conductores():
    """Muestra información de conductores"""
    st.markdown("""
        <div class="content-header">
            <h1>👥 Gestión de Conductores</h1>
            <p>Personal autorizado para operar equipos</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Total Conductores", "12", "Personal activo")
    
    with col2:
        st.metric("✅ Licencias Vigentes", "11", "91.7%")
    
    with col3:
        st.metric("⚠️ Por Vencer", "1", "8.3%")
    
    conductores = pd.DataFrame({
        'Nombre': ['Pedro Mamani', 'Félix Arce', 'Hugo Chura', 'Juan Flores', 'Carlos Mamani'],
        'Rol': ['Operador Senior', 'Operador', 'Operador', 'Operador', 'Operador'],
        'Licencia': ['Vigente', 'Vigente', 'Vigente', 'Vigente', 'Por Vencer'],
        'Equipos': [3, 2, 2, 2, 1]
    })
    
    st.dataframe(conductores, use_container_width=True, hide_index=True)

def mostrar_alertas():
    """Muestra alertas del sistema"""
    st.markdown("""
        <div class="content-header">
            <h1>⚠️ Alertas Críticas</h1>
            <p>Alertas activas del sistema</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Alertas
    st.error("🔴 **CRÍTICO:** CM-007 necesita mantenimiento urgente")
    st.warning("🟠 **ADVERTENCIA:** CM-001 ha operado 12 horas sin descanso")
    st.info("🟡 **INFORMACIÓN:** CM-004 combustible bajo - 15% del tanque")
    
    alertas_df = pd.DataFrame({
        'Equipo': ['CM-007', 'CM-001', 'CM-004', 'CM-012', 'CM-019', 'CM-025', 'CM-031'],
        'Tipo': ['Mantenimiento', 'Horas Operación', 'Combustible', 'Neumáticos', 'Aceite', 'Batería', 'Revisión'],
        'Severidad': ['Crítico', 'Advertencia', 'Información', 'Advertencia', 'Información', 'Crítico', 'Advertencia']
    })
    
    st.dataframe(alertas_df, use_container_width=True, hide_index=True)

def mostrar_carga_datos():
    """Muestra la interfaz de carga de datos"""
    st.markdown("""
        <div class="content-header">
            <h1>📤 Cargar y Analizar Datos</h1>
            <p>Sube tu archivo Excel o CSV para análisis automático</p>
        </div>
    """, unsafe_allow_html=True)
    
    if archivo is not None:
        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)
            
            st.success(f"✅ Archivo cargado correctamente - {len(df)} filas detectadas")
            
            stats = calcular_estadisticas(df)
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📋 Filas", f"{stats['filas']:,}")
            
            with col2:
                st.metric("🏷️ Columnas", f"{stats['columnas']}")
            
            with col3:
                porcentaje_nulos = (stats['valores_nulos'] / (stats['filas'] * stats['columnas']) * 100)
                st.metric("⚠️ Valores Nulos", f"{porcentaje_nulos:.1f}%")
            
            with col4:
                st.metric("✨ Calidad", f"{100 - porcentaje_nulos:.1f}%")
            
            # Gráficos automáticos
            st.markdown("### 📈 Análisis Visual Automático")
            
            graficos = generar_graficos_automaticos(
                df,
                stats['columnas_numericas'],
                stats['columnas_categoricas']
            )
            
            if graficos:
                for i, (tipo, columna, fig) in enumerate(graficos):
                    if i % 2 == 0:
                        col1, col2 = st.columns(2)
                    
                    with (col1 if i % 2 == 0 else col2):
                        st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de datos
            if mostrar_tabla:
                st.markdown("### 📋 Vista de Datos")
                st.dataframe(df.head(20), use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"❌ Error al procesar archivo: {str(e)}")
    else:
        st.info("👆 Por favor sube un archivo Excel o CSV para comenzar")

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



# ===================== INTERFAZ PRINCIPAL =====================

st.markdown("""
    <div class="header-section">
        <h1>📊 Dashboard Interactivo para Análisis de Datos</h1>
        <p style="color: #718096; font-size: 1.1rem; margin-top: 10px;">
            Sube tu archivo Excel o CSV y obtén análisis automático con gráficos dinámicos
        </p>
    </div>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown('<p class="sidebar-title">📁 Cargar Datos</p>', unsafe_allow_html=True)
    
    archivo = st.file_uploader(
        "Sube tu archivo Excel o CSV",
        type=["xlsx", "xls", "csv"],
        help="Formatos soportados: Excel (.xlsx, .xls) y CSV"
    )
    
    st.markdown('---')
    st.markdown('<p class="sidebar-title">⚙️ Opciones</p>', unsafe_allow_html=True)
    
    mostrar_tabla = st.checkbox("Mostrar tabla de datos", value=True)
    mostrar_estadisticas = st.checkbox("Mostrar estadísticas", value=True)
    
    if archivo is not None:
        st.markdown('---')
        st.markdown('<p class="sidebar-title">ℹ️ Información del archivo</p>', unsafe_allow_html=True)
        st.write(f"**Nombre:** {archivo.name}")
        st.write(f"**Tamaño:** {archivo.size / 1024:.2f} KB")

# ===================== CARGAR Y PROCESAR DATOS =====================
df = None

if archivo is not None:
    try:
        # Cargar archivo
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)
        
        # Mensaje de éxito
        st.success(f"✅ Archivo cargado correctamente - {len(df)} filas detectadas")
        
        # Calcular estadísticas
        stats = calcular_estadisticas(df)
        
        # ===================== SECCIÓN 1: MÉTRICAS =====================
        st.markdown("### 📊 Resumen de Datos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📋 Total de filas",
                f"{stats['filas']:,}",
                "registros"
            )
        
        with col2:
            st.metric(
                "🏷️ Total de columnas",
                f"{stats['columnas']}",
                "campos"
            )
        
        with col3:
            porcentaje_nulos = (stats['valores_nulos'] / (stats['filas'] * stats['columnas']) * 100)
            st.metric(
                "⚠️ Valores nulos",
                f"{stats['valores_nulos']}",
                f"{porcentaje_nulos:.1f}%"
            )
        
        with col4:
            st.metric(
                "✨ Calidad de datos",
                f"{100 - porcentaje_nulos:.1f}%",
                "completitud"
            )
        
        # ===================== SECCIÓN 2: INFORMACIÓN DE COLUMNAS =====================
        if mostrar_estadisticas:
            st.markdown("### 🔍 Descripción de Columnas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Columnas Numéricas:**")
                if stats['columnas_numericas']:
                    for col in stats['columnas_numericas']:
                        st.write(f"  • {col}")
                else:
                    st.info("No hay columnas numéricas")
            
            with col2:
                st.write("**Columnas Categóricas:**")
                if stats['columnas_categoricas']:
                    for col in stats['columnas_categoricas']:
                        st.write(f"  • {col}")
                else:
                    st.info("No hay columnas categóricas")
        
        # ===================== SECCIÓN 3: GRÁFICOS AUTOMÁTICOS =====================
        st.markdown("### 📈 Análisis Visual Automático")
        
        # Generar gráficos
        graficos = generar_graficos_automaticos(
            df,
            stats['columnas_numericas'],
            stats['columnas_categoricas']
        )
        
        if graficos:
            # Organizar en columnas
            for i, (tipo, columna, fig) in enumerate(graficos):
                if i % 2 == 0:
                    col1, col2 = st.columns(2)
                
                with (col1 if i % 2 == 0 else col2):
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No se pudieron generar gráficos automáticos")
        
        # ===================== SECCIÓN 4: TABLA DE DATOS =====================
        if mostrar_tabla:
            st.markdown("### 📋 Vista de Datos Completa")
            
            # Opciones de filtrado
            col1, col2 = st.columns(2)
            
            with col1:
                filas_mostrar = st.slider(
                    "Filas a mostrar",
                    min_value=5,
                    max_value=len(df),
                    value=min(20, len(df)),
                    step=5
                )
            
            with col2:
                columnas_seleccionadas = st.multiselect(
                    "Seleccionar columnas",
                    options=df.columns.tolist(),
                    default=df.columns.tolist()
                )
            
            # Mostrar tabla
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(
                df[columnas_seleccionadas].head(filas_mostrar),
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ===================== SECCIÓN 5: EXPORTACIÓN =====================
        st.markdown("### 📥 Exportar Resultados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            buffer = pd.ExcelWriter(f"temp_export.xlsx", engine='openpyxl')
            df.to_excel(buffer, sheet_name='Datos', index=False)
            st.download_button(
                label="📥 Descargar Excel",
                data=open(f"temp_export.xlsx", "rb").read() if False else b'',
                file_name=f"datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            st.download_button(
                label="📊 Descargar Resumen",
                data=f"Análisis de: {archivo.name}\n\nEstadísticas:\n- Filas: {stats['filas']}\n- Columnas: {stats['columnas']}\n- Calidad: {100 - porcentaje_nulos:.1f}%",
                file_name=f"resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Error al procesar archivo: {str(e)}")
        st.info("Verifica que el archivo esté en el formato correcto")

else:
    # ===================== VISTA SIN ARCHIVO =====================
    st.markdown("""
        <div class="header-section">
            <div style="text-align: center; padding: 40px;">
                <h2 style="color: #667eea;">👆 Sube un archivo para comenzar</h2>
                <p style="color: #718096; font-size: 1.1rem; margin-top: 15px;">
                    Compatible con archivos Excel (.xlsx, .xls) y CSV
                </p>
                <div style="margin-top: 30px; padding: 20px; background: #f7fafc; border-radius: 10px;">
                    <p><strong>¿Qué puedes hacer?</strong></p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>📊 Analizar datos automáticamente</li>
                        <li>📈 Generar gráficos dinámicos</li>
                        <li>🔍 Detectar patrones y tendencias</li>
                        <li>📥 Exportar resultados</li>
                    </ul>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)