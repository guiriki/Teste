from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# Ferramenta de busca
search_tool = DuckDuckGoSearchRun()

# Agente de busca de artigos
search_agent = Agent(
    role="Buscador de Artigos",
    goal="Buscar artigos relevantes sobre o tema informado",
    tools=[search_tool],
    verbose=True
)

# Agente de resumo
summary_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # Ou outro modelo disponível
summary_agent = Agent(
    role="Resumidor de Artigos",
    goal="Resumir artigos encontrados de forma objetiva e clara",
    llm=summary_llm,
    verbose=True
)

# Task pipeline
def buscar_e_resumir_artigos(tema):
    # 1. Buscar links de artigos
    resultado_busca = search_agent.run(f"artigos sobre {tema}")
    links = [item['href'] for item in resultado_busca[:3]]  # Limitar a 3 artigos

    # 2. Para cada link, gerar um resumo
    resumos = []
    for link in links:
        texto = search_tool.run(link)  # Busca texto do artigo
        resumo = summary_agent.run(f"Resuma este artigo: {texto}")
        resumos.append({'link': link, 'resumo': resumo})

    return resumos

# Exemplo de uso
if __name__ == "__main__":
    tema = "inteligência artificial"
    resumos = buscar_e_resumir_artigos(tema)
    for idx, item in enumerate(resumos):
        print(f"Artigo {idx+1}: {item['link']}\nResumo: {item['resumo']}\n")
