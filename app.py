import requests
from bs4 import BeautifulSoup
import feedgenerator

# Função para extrair as informações dos artigos
def get_article_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Pegando as informações do Open Graph
        title = soup.find("meta", property="og:title")["content"]
        description = soup.find("meta", property="og:description")["content"]
        image = soup.find("meta", property="og:image")["content"]
        article_url = soup.find("meta", property="og:url")["content"]
        published_time = soup.find("meta", property="article:published_time")["content"]
        
        return {
            "title": title,
            "description": description,
            "image": image,
            "url": article_url,
            "published_time": published_time
        }
    else:
        print(f"Erro ao acessar o artigo: {response.status_code}")
        return None

# Função para gerar o feed RSS
def generate_rss():
    # URL inicial do site ou da página de listagem de artigos
    url = "https://www.tribunaonline.net/taquaritinga-recebe-premio-excelencia-educacional-por-destaque-na-alfabetizacao/"
    
    # Extrair os dados do artigo
    article_data = get_article_data(url)

    if article_data:
        # Criação do feed RSS
        feed = feedgenerator.Rss201rev2Feed(
            title="Jornal Tribuna Taquaritinga/SP",
            link="https://www.tribunaonline.net/",
            description="Notícias do Jornal Tribuna Taquaritinga"
        )

        # Adicionando o artigo ao feed
        feed.add_item(
            title=article_data["title"],
            link=article_data["url"],
            description=article_data["description"],
            pubdate=article_data["published_time"],
            unique_id=article_data["url"]
        )

        # Salvando o feed em um arquivo XML
        with open("feed.xml", "w", encoding="utf-8") as f:
            f.write(feed.writeString("utf-8"))

        print("Feed RSS gerado com sucesso!")

# Chamar a função para gerar o RSS
generate_rss()
