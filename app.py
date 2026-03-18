import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configurar página
st.set_page_config(
    page_title="Dashboard - Gestión de Alquiler",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("📊 Dashboard - Gestión de Alquiler de Camionetas")

# Sidebar - Carga de datos
st.sidebar.header("📁 Gestión de datos")

# Opción 1: Cargar archivo
archivo = st.sidebar.file_uploader(
    "Sube tu archivo Excel o CSV",
    type=["xlsx", "csv"],
    key="data_upload"
)

# Crear datos de ejemplo si no hay archivo
if archivo is None:
    st.info("📌 **Cargando datos de exemplo...**")
    
    # Datos de ejemplo
    datos_ejemplo = {
        'ID': ['CM-001', 'CM-002', 'CM-003', 'CM-004', 'CM-005'],
        'Modelo': ['Camión Volvo', 'Camión MAN', 'Camión Scania', 'Camión Volvo', 'Camión MAN'],
        'Empresa': ['Minería Topaquepala', 'Cerro Verde', 'Las Bambas', 'Minería Topaquepala', 'Cerro Verde'],
        'Estado': ['Activo', 'Activo', 'Mantenimiento', 'Activo', 'Inactivo'],
        'Costo Diario': [5000, 4500, 5500, 5000, 4500],
        'Responsable': ['Ing. Quispe R.', 'Ing. López M.', 'Ing. García H.', 'Ing. Quispe R.', 'Ing. López M.'],
        'Conductor': ['Pedro Mamani', 'Félix Arce', 'Hugo Chura', 'Juan Flores', 'Carlos Mamani']
    }
    df = pd.DataFrame(datos_ejemplo)
else:
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)
        st.sidebar.success("✅ Archivo cargado correctamente")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")
        df = None

# Mostrar dashboard si hay datos
if df is not None:
    
    # ==================== FILTROS ====================
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por Estado
    if 'Estado' in df.columns:
        estados = ['Todos'] + df['Estado'].unique().tolist()
        estado_filtro = st.sidebar.selectbox("Estado", estados)
        if estado_filtro != 'Todos':
            df = df[df['Estado'] == estado_filtro]
    
    # Filtro por Empresa
    if 'Empresa' in df.columns:
        empresas = ['Todas'] + df['Empresa'].unique().tolist()
        empresa_filtro = st.sidebar.selectbox("Empresa", empresas)
        if empresa_filtro != 'Todas':
            df = df[df['Empresa'] == empresa_filtro]
    
    # ==================== MÉTRICAS ====================
    st.header("📈 Resumen General")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_equipos = len(df)
        st.metric(
            label="Total Equipos",
            value=total_equipos,
            delta="Flota disponible",
            delta_color="off"
        )
    
    with col2:
        if 'Estado' in df.columns:
            activos = len(df[df['Estado'] == 'Activo'])
            st.metric(
                label="Equipos Activos",
                value=activos,
                delta=f"{round(activos/total_equipos*100, 1)}% del total"
            )
    
    with col3:
        if 'Costo Diario' in df.columns:
            costo_total = df['Costo Diario'].sum()
            st.metric(
                label="Costo Total Diario",
                value=f"S/ {costo_total:,.0f}",
                delta="Inversión total",
                delta_color="off"
            )
    
    with col4:
        if 'Responsable' in df.columns:
            responsables = df['Responsable'].nunique()
            st.metric(
                label="Responsables",
                value=responsables,
                delta="Personal asignado"
            )
    
    # ==================== GRÁFICOS ====================
    st.header("📊 Análisis Visual")
    
    col1, col2 = st.columns(2)
    
    # Gráfico 1: Equipos por Estado
    with col1:
        if 'Estado' in df.columns:
            estado_count = df['Estado'].value_counts()
            fig1 = px.pie(
                values=estado_count.values,
                names=estado_count.index,
                title="Distribución por Estado",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Equipos por Empresa
    with col2:
        if 'Empresa' in df.columns:
            empresa_count = df['Empresa'].value_counts()
            fig2 = px.bar(
                x=empresa_count.index,
                y=empresa_count.values,
                title="Equipos por Empresa",
                labels={'x': 'Empresa', 'y': 'Cantidad'},
                color_discrete_sequence=['#636EFA']
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # ==================== TABLA DE DATOS ====================
    st.header("📋 Detalle de Equipos")
    
    # Mostrar tabla
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Costo Diario': st.column_config.NumberColumn(format="S/ %d")
        }
    )
    
    # ==================== DESCARGA ====================
    st.header("📥 Exportar Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Descargar como CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar como CSV",
            data=csv,
            file_name=f"equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Descargar como Excel
        import io
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Equipos', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Equipos']
            
            # Estilos
            fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            font = Font(bold=True, color="FFFFFF")
            
            for cell in worksheet[1]:
                cell.fill = fill
                cell.font = font
        
        buffer.seek(0)
        st.download_button(
            label="📥 Descargar como Excel",
            data=buffer.getvalue(),
            file_name=f"equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.warning("❌ No se pudo cargar el archivo. Verifica el formato.")