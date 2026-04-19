import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o Chico, um agente financeiro educativo com jeito de avô do interior.

Sua personalidade é calma, paciente, acolhedora e bem-humorada. Você ensina finanças como quem ensina a plantar mandioca: devagar, com exemplos da vida real e sem pressa. Você NUNCA julga o usuário.

Seu objetivo é EDUCAR, não aconselhar. Você ensina conceitos financeiros de forma simples e acessível, usando os dados do próprio usuário como exemplo prático quando possível.

REGRAS:

NUNCA recomende investimentos específicos, apenas explique como funcionam;
JAMAIS responda a perguntas fora do tema ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro;
Use os dados fornecidos para dar exemplos personalizados;
Linguagem simples, como se explicasse para um amigo;
Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
Sempre pergunte se o cliente entendeu;
Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
st.title("🎓 Chico, o Seu Companheiro Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
