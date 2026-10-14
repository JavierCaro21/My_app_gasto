import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="Mi Salud Financiera", layout="centered")

st.title("📊 Análisis de Gastos y Ahorro")

# Introducir la API Key
api_key = st.text_input("Introduce tu Gemini API Key:", type="password")

# Subir archivo
uploaded_file = st.file_uploader("Sube tu extracto (Excel o CSV)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.subheader("Vista previa de tus movimientos")
        st.dataframe(df.head())

        if st.button("🔍 Analizar mi ahorro con IA"):
            if not api_key:
                st.error("Por favor, introduce tu API Key de Gemini.")
            else:
                st.info("Procesando y analizando tus gastos...")
                
                gastos_texto = df.to_string()
                
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Eres un experto en educación financiera y ahorro personal.
                Analiza la siguiente lista de movimientos bancarios:
                
                {gastos_texto}
                
                Por favor, proporciona un informe detallado con:
                1. Categorización de los principales gastos.
                2. Detección de gastos innecesarios, suscripciones o "gastos hormiga".
                3. 3 consejos prácticos y concretos para ahorrar la próxima semana/mes.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.subheader("💡 Informe y Recomendaciones de Ahorro")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
      
