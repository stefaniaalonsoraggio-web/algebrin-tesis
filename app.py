import streamlit as st
import google.generativeai as genai
import os

st.title("📐 Algebrín - Tu Tutor de Álgebra")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- NUEVO: Función para subir los PDFs a la memoria de Google ---
@st.cache_resource
def cargar_guias():
    # ACA PONÉ LOS NOMBRES EXACTOS DE TUS ARCHIVOS COMO ESTÁN EN GITHUB
    mis_guias = ["tp_vectores.pdf", "tp_matrices.pdf"] 
    
    archivos_listos = []
    for archivo in mis_guias:
        if os.path.exists(archivo):
            # Esto manda el PDF a Google
            archivo_subido = genai.upload_file(path=archivo)
            archivos_listos.append(archivo_subido)
            
    return archivos_listos

# Ejecutamos la función para tener los archivos listos
documentos_ia = cargar_guias()
# -----------------------------------------------------------------

instrucciones = "Sos Algebrín, tutor de Álgebra. Usá el método socrático y NUNCA des la respuesta final..."
modelo = genai.GenerativeModel(
    model_name='gemini-3.1-pro-preview', # O el flash si preferís por los límites
    system_instruction=instrucciones
)

# --- NUEVO: Le inyectamos los PDFs en el primer mensaje oculto ---
if "chat" not in st.session_state:
    # Si logramos subir documentos, se los pasamos como contexto inicial
    si_hay_docs = documentos_ia + ["Acá tenés las guías de la materia. Usalas para basar tus explicaciones."]
    
    st.session_state.chat = modelo.start_chat(
        history=[
            {"role": "user", "parts": si_hay_docs if documentos_ia else ["Hola"]},
            {"role": "model", "parts": ["Entendido. Ya leí las guías y las usaré estrictamente para responder a los alumnos."]}
        ]
    )
# -----------------------------------------------------------------

# Mostrar mensajes en la pantalla
for mensaje in st.session_state.chat.history[2:]: # Salteamos los 2 primeros mensajes ocultos de configuración
    rol = "user" if mensaje.role == "user" else "assistant"
    with st.chat_message(rol):
        st.markdown(mensaje.parts[0].text)

pregunta_alumno = st.chat_input("Preguntale a Algebrín sobre la guía...")

if pregunta_alumno:
    with st.chat_message("user"):
        st.markdown(pregunta_alumno)
    
    with st.chat_message("assistant"):
        try:
            respuesta = st.session_state.chat.send_message(pregunta_alumno)
            st.markdown(respuesta.text)
        except Exception as e:
            st.error("¡Uf! Muchos alumnos preguntando al mismo tiempo. Esperá un minutito y volvé a intentar.")
