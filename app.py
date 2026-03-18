import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ===================== CONFIGURACIÓN =====================
st.set_page_config(
    page_title="Dashboard Interactivo",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        for col in columnas_numericas[:4]:  # Máximo 4 gráficos
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
        for col in columnas_categoricas[:3]:  # Máximo 3 gráficos
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