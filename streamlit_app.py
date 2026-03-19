import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ===================== CONFIGURACIÓN PAGE =====================
st.set_page_config(
    page_title="EXOR - Gestión de Flota",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS PERSONALIZADO =====================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
    }
    .metric-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f2937;
        font-size: 28px;
        margin-bottom: 10px;
    }
    h2 {
        color: #1f2937;
        font-size: 22px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===================== INICIALIZAR SESSION STATE =====================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'file_info' not in st.session_state:
    st.session_state.file_info = None

# ===================== SIDEBAR =====================
with st.sidebar:
    st.title("🏢 EXOR")
    st.write("Gestión de Flota")
    st.divider()
    
    # Subir archivo
    st.subheader("📤 Cargar Archivo")
    uploaded_file = st.file_uploader("Selecciona tu archivo Excel o CSV", type=['xlsx', 'csv', 'xls'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)
            
            st.session_state.file_info = {
                'nombre': uploaded_file.name,
                'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'filas': len(st.session_state.df),
                'columnas': len(st.session_state.df.columns)
            }
            st.success("✅ Archivo cargado correctamente")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
    
    st.divider()
    
    # Información del archivo
    if st.session_state.file_info:
        st.subheader("📊 Información")
        info = st.session_state.file_info
        st.write(f"**Archivo:** {info['nombre']}")
        st.write(f"**Fecha:** {info['fecha']}")
        st.write(f"**Filas:** {info['filas']}")
        st.write(f"**Columnas:** {info['columnas']}")

# ===================== HEADER =====================
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("📦 Inventario de Equipos")
    st.write("*Gestión completa de la flota EXOR*")

with col2:
    today = datetime.now().strftime("%d de %b %Y")
    st.write(f"📅 {today}")

st.divider()

# ===================== SI NO HAY DATOS =====================
if st.session_state.df is None:
    st.info("👆 **Carga un archivo Excel o CSV** desde el panel izquierdo para comenzar")
    st.stop()

# ===================== PROCESAMIENTO DE DATOS =====================
df = st.session_state.df

# Detectar columnas importantes
estado_col = None
empresa_col = None
linea_col = None

for col in df.columns:
    if 'estado' in col.lower() or 'status' in col.lower():
        estado_col = col
    if 'empresa' in col.lower() or 'company' in col.lower():
        empresa_col = col
    if 'línea' in col.lower() or 'linea' in col.lower():
        linea_col = col

# ===================== TABS =====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Resumen", 
    "📋 Datos", 
    "📈 Gráficas", 
    "📅 Calendarios",
    "⚙️ Configuración"
])

# ===================== TAB 1: RESUMEN =====================
with tab1:
    # Cards de estadísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📦 Total de Equipos",
            len(df),
            "registros"
        )
    
    with col2:
        if estado_col:
            activos = len(df[df[estado_col].str.lower() == 'activo'])
            st.metric(
                "✅ Equipos Activos",
                activos,
                f"{(activos/len(df)*100):.1f}%"
            )
        else:
            st.metric("✅ Equipos Activos", "N/A", "")
    
    with col3:
        st.metric(
            "📊 Empresas",
            df[empresa_col].nunique() if empresa_col else "N/A",
            "únicas"
        )
    
    with col4:
        st.metric(
            "📋 Columnas",
            len(df.columns),
            "atributos"
        )
    
    st.divider()
    
    # Filas por empresa
    if empresa_col:
        st.subheader("Equipos por Empresa")
        empresa_counts = df[empresa_col].value_counts()
        
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            fig = px.bar(
                x=empresa_counts.index,
                y=empresa_counts.values,
                labels={'x': 'Empresa', 'y': 'Cantidad'},
                color=empresa_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                values=empresa_counts.values,
                names=empresa_counts.index,
                title="Distribución"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Estado de equipos
    if estado_col:
        st.subheader("Estado de Equipos")
        estado_counts = df[estado_col].value_counts()
        
        colors = {
            'activo': '#10b981',
            'mantenimiento': '#f59e0b',
            'inactivo': '#ef4444'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Resumen:**")
            for estado, count in estado_counts.items():
                porcentaje = (count / len(df) * 100)
                st.write(f"• **{estado.title()}:** {count} ({porcentaje:.1f}%)")
        
        with col2:
            fig = px.pie(
                values=estado_counts.values,
                names=estado_counts.index,
                title="Distribución de Estados"
            )
            st.plotly_chart(fig, use_container_width=True)

# ===================== TAB 2: DATOS =====================
with tab2:
    st.subheader("📋 Tabla de Datos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if empresa_col:
            selected_empresa = st.multiselect(
                "Filtrar por Empresa",
                df[empresa_col].unique(),
                default=df[empresa_col].unique()
            )
        else:
            selected_empresa = None
    
    with col2:
        if estado_col:
            selected_estado = st.multiselect(
                "Filtrar por Estado",
                df[estado_col].unique(),
                default=df[estado_col].unique()
            )
        else:
            selected_estado = None
    
    with col3:
        search = st.text_input("🔍 Buscar...", "")
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_empresa and empresa_col:
        filtered_df = filtered_df[filtered_df[empresa_col].isin(selected_empresa)]
    
    if selected_estado and estado_col:
        filtered_df = filtered_df[filtered_df[estado_col].isin(selected_estado)]
    
    if search:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Exportar
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 Descargar como CSV",
            csv,
            "datos.csv",
            "text/csv",
            key='download-csv'
        )
    
    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False)
        st.download_button(
            "📥 Descargar como Excel",
            buffer.getvalue(),
            "datos.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key='download-excel'
        )

# ===================== TAB 3: GRÁFICAS =====================
with tab3:
    st.subheader("📈 Análisis Gráfico")
    
    col1, col2 = st.columns(2)
    
    # Gráfica 1: Columnas numéricas
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        with col1:
            st.write("**Distribución de valores numéricos**")
            selected_col = st.selectbox("Selecciona columna", numeric_cols, key='graph1')
            fig = px.histogram(df, x=selected_col, nbins=20, title=f"Distribución de {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    # Gráfica 2: Comparativas
    if empresa_col and numeric_cols:
        with col2:
            st.write("**Comparativa por Empresa**")
            selected_metric = st.selectbox("Métrica", numeric_cols, key='graph2')
            fig = px.box(df, x=empresa_col, y=selected_metric, title=f"{selected_metric} por Empresa")
            st.plotly_chart(fig, use_container_width=True)

# ===================== TAB 4: CALENDARIO =====================
with tab4:
    st.subheader("📅 Calendario")
    st.info("Sección de calendario disponible si el archivo contiene columnas de fecha")

# ===================== TAB 5: CONFIGURACIÓN =====================
with tab5:
    st.subheader("⚙️ Configuración")
    
    st.write("**Información del Dataset:**")
    st.write(f"- Total de filas: {len(df)}")
    st.write(f"- Total de columnas: {len(df.columns)}")
    st.write(f"- Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    st.write("\n**Columnas detectadas:**")
    st.write(df.columns.tolist())
    
    st.write("\n**Primeras filas:**")
    st.dataframe(df.head(), use_container_width=True)
