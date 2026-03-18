import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporte de Alquiler", layout="wide")

st.title("📊 Reporte de Alquiler de Camionetas")

# Subir archivo
archivo = st.file_uploader("Sube tu archivo Excel o CSV", type=["xlsx", "csv"])

if archivo is not None:
    try:
        # Leer archivo
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)
        
        st.success("✅ Archivo cargado correctamente")
        
        # Mostrar datos
        st.subheader("📋 Vista de datos")
        st.dataframe(df, use_container_width=True)
        
        # Resumen
        st.subheader("📊 Resumen")
        st.write(f"Total de filas: {len(df)}")
        st.write(f"Total de columnas: {len(df.columns)}")
        
    except Exception as e:
        st.error(f"❌ Error al procesar archivo: {e}")
else:
    st.info("👆 Por favor sube un archivo para comenzar")