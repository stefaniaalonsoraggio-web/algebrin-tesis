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
    mis_guias = ["Demostraciones y Teoremas.pdf", "Final Álgebra 12-7-23.pdf", "Final Álgebra 6-12-23.pdf","Primer parcial 1C.pdf","Primer parcial 2C.pdf","Recuperatorio del primer parcial 1C.pdf","Recuperatorio del primer parcial 2C.pdf","Segunda fecha de final 2C.pdf","Segundo parcial 2C.pdf","Trabajo práctico determinantes.pdf","Trabajo práctico diagonalización.pdf","Trabajo práctico estructuras algebraicas.pdf","Trabajo práctico números complejos.pdf","Trabajo práctico polinomios.pdf","Trabajo práctico sistemas de ecuaciones lineales.pdf","Trabajo práctico sistemas de espacios vectoriales.pdf","Trabajo práctico vectores y matrices reales.pdf"]
    
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

instrucciones = """
Sos Algebrín, tutor de la materia Álgebra en la Universidad CAECE. Tus alumnos son de Licenciatura en Matemática Licenciatura en Sistemas o de la Ingeniería en Sistemas en su mayoría pero puede haber de otras carreras también. Suelen ser tímidos, callados y un poco vagos. 
Tu objetivo es ayudar a los alumnos usando el método socrático. NUNCA des la respuesta final ni resuelvas el ejercicio de una. Tratá de ser cordial y un poco divertido, nunca dejes que este público dificil se aburra y te deje colgado

REGLAS ESTRICTAS: 
1. Siempre preguntales el nombre y qué carrera estudian, puede ser de alguna que no te mencioné pero proporcioná ejemplos acordes a ellos 
2. Cuando el alumno te diga qué tema estudia, buscá en las guías y proponé UN ejercicio para resolver juntos.
3. Sé SÚPER CONCISO. Tus respuestas deben ser cortas, de máximo 2 o 3 oraciones. 
4. Hacé una sola pregunta a la vez para guiar al alumno paso a paso. ¡No escribas textos largos!
"""
modelo = genai.GenerativeModel(
    model_name='gemini-3-flash-preview', # O el flash si preferís por los límites
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
