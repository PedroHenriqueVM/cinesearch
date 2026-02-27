from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b4931eecf6131e5cd1ec663072006203"
BASE_URL = "https://api.themoviedb.org/3"


def buscar_filme(nome):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": nome,
        "language": "pt-BR"
    }
    return requests.get(url, params=params).json()


def buscar_por_genero(genero_id):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genero_id,
        "language": "pt-BR"
    }
    return requests.get(url, params=params).json()


def detalhes_filme(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR"
    }
    return requests.get(url, params=params).json()


def provedores_filme(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {
        "api_key": API_KEY
    }
    dados = requests.get(url, params=params).json()

    if "results" in dados and "BR" in dados["results"]:
        return dados["results"]["BR"].get("flatrate", [])
    return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/buscar", methods=["POST"])
def buscar():
    nome = request.form.get("nome")
    genero = request.form.get("genero")

    if nome:
        dados = buscar_filme(nome)
    elif genero:
        dados = buscar_por_genero(genero)
    else:
        dados = None

    filmes_detalhados = []

    if dados and "results" in dados:
        for filme in dados["results"][:6]:
            detalhes = detalhes_filme(filme["id"])
            provedores = provedores_filme(filme["id"])

            filmes_detalhados.append({
                "titulo": detalhes.get("title"),
                "sinopse": detalhes.get("overview"),
                "duracao": detalhes.get("runtime"),
                "nota": detalhes.get("vote_average"),
                "classificacao": detalhes.get("adult"),
                "banner": detalhes.get("backdrop_path"),
                "provedores": provedores
            })

    return render_template("resultados.html", filmes=filmes_detalhados)

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)