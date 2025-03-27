import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime
from flask import Flask, Response

app = Flask(__name__)

# Função para pegar os artigos
def get_articles():
    url = "https://www.tribunaonline.net/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Para evitar bloqueios

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")
        
        print(f"Artigos encontrados: {len(articles)}")  # Adicionando depuração aqui
        
        article_list = []
        for article in articles[:5]:  # Pegando os 5 primeiros artigos
            title = article.find("h2").text if article.find("h2") else "Sem título"
            link = article.find("a")["href"] if article.find("a") else None
            description = article.find("p").text if article.find("p") else "Sem descrição"
            image = article.find("img")["src"] if article.find("img") else None
            
            article_list.append({
                'title': title,
                'link': link,
                'description': description,
                'image': image
            })
        
        return article_list
    else:
        print("Erro ao acessar o site:", response.status_code)
        return []

# Função para criar o Feed RSS
def create_rss():
    articles = get_articles()
    
    if not articles:
        print("Nenhum artigo encontrado!")
        return "Nenhum artigo encontrado!"  # Adicionando uma mensagem mais explícita
    
    fg = FeedGenerator()
    fg.title("Tribuna Online - Notícias")
    fg.link(href="https://www.tribunaonline.net/")
    fg.description("Feed RSS personalizado do Tribuna Online")
    fg.language("pt-br")
    fg.generator("python-feedgen")
    fg.lastBuildDate(datetime.datetime.now())

    # Adicionando artigos ao feed
    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(article['description'])
        
        if article['image']:
            fe.enclosure(url=article['image'], type="image/jpeg")

    # Gerar o XML do feed
    rss_feed = fg.rss_str(pretty=True)
    
    return rss_feed

@app.route('/rss')
def rss_feed():
    print("Acessando o feed RSS...")  # Adicionando depuração para garantir que a rota foi chamada
    rss = create_rss()
    return Response(rss, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(debug=True)
