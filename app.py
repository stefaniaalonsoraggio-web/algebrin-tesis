import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.title("📐 Algebrín - Tu Tutor de Álgebra")
st.caption("Asistente virtual para la materia Álgebra Lineal")

# 2. Conectamos con Google (Acá va tu API Key real)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Configuramos a Algebrín
instrucciones = "Sos Algebrín, tutor de Álgebra. Usá el método socrático y NUNCA des la respuesta final..."
modelo = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=instrucciones
)

# 3. Memoria del chat (para que recuerde la charla actual)
if "chat" not in st.session_state:
    st.session_state.chat = modelo.start_chat(history=[])

# Mostrar mensajes anteriores en la web
for mensaje in st.session_state.chat.history:
    rol = "user" if mensaje.role == "user" else "assistant"
    with st.chat_message(rol):
        st.markdown(mensaje.parts[0].text)

# 4. Caja de texto para que el alumno escriba
pregunta_alumno = st.chat_input("Preguntale a Algebrín sobre la guía...")

if pregunta_alumno:
    # Mostramos lo que escribió el alumno
    with st.chat_message("user"):
        st.markdown(pregunta_alumno)
    
    # Le mandamos la pregunta a Gemini y mostramos la respuesta
    with st.chat_message("assistant"):
        respuesta = st.session_state.chat.send_message(pregunta_alumno)
        st.markdown(respuesta.text)
        
        # ¡Acá más adelante podemos sumar el código para guardar los datos de tu tesis!
