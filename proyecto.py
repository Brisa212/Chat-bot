import streamlit as st #importamos la librería streamlit
from groq import Groq #Nueva importación 
#Le damos un titulo a la pestaña de la web 

st.set_page_config(page_title= " Mi Chat de IA", page_icon= "🍕") 

#Título de la página
st.title("Mi primera aplicación con Streamlit")

#Ingreso de datos 

nombre = st.text_input("¿Cómo te llamas?")

#Crear botón 
if st.button("Saludar") :
    st.write(f"Hola {nombre}: Gracias por visitar mi aplicación ")

#Posiciones          0                  1           2         
MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
#Creando función con el diseño de la pagina

#Nos conecta a la API, crear un usuario

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obteniendo la clave de nuestro archivo
    return Groq(api_key = clave_secreta) #Crea el Usuario

#Cliente = usuario a groq | modelo de la IA seleccionada / Mensaje del Usuario 

def configurar_modelo(cliente, modelo, mensajeDeEntrada ) :
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user", "content" : mensajeDeEntrada}], 
        stream = True
    )

#Simula un Historial de mensaje 
def inicializar_estado() : 
    #Si "mensajes" no esta en st.session_statest
    if "mensajes" not in st.session_state :
        st.session_state.mensajes = [] #Memoria de Mensajes

def actualizar_historial(rol, contenido, avatar):
    #El metodo apped()agrega un elemento a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes :
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])
        st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #Agrupamos los mensajes en el area del chat
    with contenedorDelChat : mostrar_historial()



def configurar_pagina() :
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegí un modelo", 
        MODELO,
        index=0
    )
    return seleccion

def generar_respuestas (chat_completo):
    respuesta_completa = "" #texto vacío
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa 


def main():

    modelo = configurar_pagina()
    #st.write(f"El usuario eligio el modelo {modelo})
    clienteUsuario = crear_usuario_groq()
    inicializar_estado() #Llama a la función historial
    area_chat() #Creamos el sector para ver los mensajes
    mensaje = st.chat_input("Escribi tu mensaje: ")
    #st.write(f"usuario: {mensaje}")

    #Verifica si el mensaje tiene contenido

    if mensaje: 
        actualizar_historial("user", mensaje, "😊")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "😁")
    # configurar_modelo(clienteUsuario, modelo, mensaje)
        #print(mensaje)
        st.rerun()
#Indicamos que nuestra funcion principal es main

if __name__ == "__main__":
    main()