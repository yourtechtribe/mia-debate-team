# filename: debate_app.py
import streamlit as st
import debatemanager
import ststreamer
from contextlib import redirect_stdout

from dotenv import load_dotenv
import os
import json

# Carga las variables de entorno
load_dotenv()

# Define el modelo y obtén la clave API del archivo .env
llm = "gpt-3.5-turbo-0125"  # O cualquier otro modelo que desees usar, como gpt-4-1106-preview       
api_key = os.getenv('OPENAI_API_KEY')  # Obtiene la clave API directamente

# Función para crear y cargar el equipo de debate
def create_debate_team(api_key):
    dm = debatemanager.debate(api_key)
    dm.load_team()
    return dm
    
# Función para capturar la salida de consola
def capture_console_output(func, *args, **kwargs):
    f = ststreamer.ObservableStringIO()
    with redirect_stdout(f):
        func(*args, **kwargs)
    output = f.getvalue()
    return output

# Inicializar el estado de la sesión
if 'dm' not in st.session_state:
    st.session_state['dm'] = None

# Título de la app
st.title("M.IA - Debate Agente VS Agente")

# Si se ha proporcionado la clave API, crea y carga el equipo de debate
if api_key and st.session_state['dm'] is None:
    with st.spinner("Creando equipo de debate..."):
        st.session_state['dm'] = create_debate_team(api_key)

# Una vez creado el equipo de debate, solicita una proposición de debate
if st.session_state['dm']:
    proposition = st.text_input("¿Qué quieres debatir hoy?:")
    if proposition:
        full_proposition = f"Debate sobre el tema: {proposition}"
        with st.spinner(f"Debatiendo el tema: {proposition}. Un momento, por favor."):
            # Redirige la salida de consola y realiza el debate
            output = capture_console_output(st.session_state['dm'].do_debate, full_proposition)
