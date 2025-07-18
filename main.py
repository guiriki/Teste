import requests
from duckduckgo_search import DDGS
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def buscar_e_resumir_artigos(tema: str, num_artigos: int = 3):
    """Busca links de artigos e retorna um pequeno resumo de cada um."""
    resultados = []
    with DDGS() as ddgs:
        for r in ddgs.text(tema, max_results=num_artigos):
            resultados.append(r.get("href"))
            if len(resultados) >= num_artigos:
                break

    resumos = []
    for link in resultados:
        try:
            resp = requests.get(link, timeout=10)
            resp.raise_for_status()
            parser = HtmlParser.from_string(
                resp.text, link, Tokenizer("portuguese"))
            summarizer = LsaSummarizer()
            sentences = summarizer(parser.document, 3)
            resumo = " ".join(str(s) for s in sentences)
        except Exception as exc:
            resumo = f"Erro ao processar artigo: {exc}"
        resumos.append({"link": link, "resumo": resumo})
    return resumos


if __name__ == "__main__":
    tema = "inteligência artificial"
    resumos = buscar_e_resumir_artigos(tema)
    for idx, item in enumerate(resumos, 1):
        print(f"Artigo {idx}: {item['link']}\nResumo: {item['resumo']}\n")
