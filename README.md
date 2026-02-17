# 🤖 Smart FAQ Bot - Automação de Atendimento (NLP)

Uma ferramenta de Inteligência Artificial baseada em Processamento de Linguagem Natural (NLP), desenvolvida para automatizar o suporte de nível 1 e responder dúvidas frequentes de forma ágil.

## Objetivo
Atuar como um agente conversacional inteligente que interpreta a intenção do usuário, reduzindo a fila de atendimento humano. O sistema realiza:
- Interpretação de linguagem natural via vetorização de texto.
- Recuperação de respostas baseada em similaridade semântica.
- Recomendação de opções interativas quando a pergunta é ambígua.

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Streamlit:** Para construção da interface de chat com histórico dinâmico.
- **Scikit-Learn:** Para implementação das técnicas de NLP (`TfidfVectorizer` e `cosine_similarity`).
- **Pandas:** Para manipulação e leitura da base de conhecimento via CSV.

## Como Funciona
O modelo não utiliza fluxogramas engessados. Ele aplica a técnica matemática de **TF-IDF (Term Frequency-Inverse Document Frequency)** para transformar a base de perguntas (`faq.csv`) e a dúvida do usuário em vetores. 

Em seguida, calcula a **Similaridade de Cosseno** para encontrar a melhor correspondência:
- **Alta Confiança (>60%):** O bot envia a resposta exata imediatamente.
- **Média Confiança (>10%):** O bot sugere até 3 botões interativos com perguntas aproximadas para o usuário escolher.
- **Baixa Confiança:** O bot solicita graciosamente que o usuário reformule a pergunta.

## Como Executar Localmente
1. Clone o repositório.
2. Certifique-se de ter o arquivo `faq.csv` na mesma pasta do projeto.
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
4. Execute o bot:
   ```bash
   streamlit run bot.py