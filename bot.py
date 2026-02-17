import pandas as pd
import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🤖 Chatbot de Teste")

try:
    df = pd.read_csv("faq.csv", sep=",")
except:
    st.error("Erro ao ler o arquivo faq.csv.")
    st.stop()

def responder_pergunta(pergunta_usuario, dados_banco):
    todas_perguntas = dados_banco['Perguntas'].tolist() + [pergunta_usuario]

    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(todas_perguntas)

    vetor_usuario = matriz[-1]
    vetor_banco = matriz[:-1]

    similaridades = cosine_similarity(vetor_usuario, vetor_banco)

    indice_maximo = similaridades.argmax()
    nivel_confianca = similaridades[0][indice_maximo]
    ranking_decrescente = similaridades[0].argsort()[::-1]

    sugestoes = []
    for i in ranking_decrescente[:3]:
        if similaridades[0][i] > 0.1: 
            sugestoes.append(dados_banco.iloc[i]['Perguntas'])

    if nivel_confianca > 0.6: 
        return dados_banco.iloc[indice_maximo]['Respostas']
    
    elif len(sugestoes) > 0:
        return sugestoes   
    else:
        return "Desculpe, não entendi a pergunta. Pode tentar com outras palavras?"

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua dúvida...")

if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.historico.append({"role": "user", "content": pergunta})
    
    resposta = responder_pergunta(pergunta, df)

    if isinstance(resposta, list):
        st.session_state.sugestoes_ativas = resposta 
        st.session_state.historico.append({"role": "assistant", "content": "Encontrei algumas opções parecidas, selecione abaixo:"})
    else:
        with st.chat_message("assistant"):
            st.markdown(resposta)
        st.session_state.historico.append({"role": "assistant", "content": resposta})
        if "sugestoes_ativas" in st.session_state:
            del st.session_state.sugestoes_ativas

if "sugestoes_ativas" in st.session_state:
    st.info("💡 Opções encontradas:")
    cols = st.columns(len(st.session_state.sugestoes_ativas))
    
    for i, opcao in enumerate(st.session_state.sugestoes_ativas):
        with cols[i]:
            if st.button(opcao, key=f"btn_{i}"):
                resposta_final = responder_pergunta(opcao, df)
                st.session_state.historico.append({
                    "role": "assistant", 
                    "content": f"**Opção escolhida:** {opcao}\n\n{resposta_final}"
                })
                del st.session_state.sugestoes_ativas
                st.rerun()