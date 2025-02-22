from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from trie import Trie
import pandas as pd
import pickle
import os
import gdown
import httpx
import asyncio

load_dotenv()
api_key = os.getenv("AUTH_TOKEN")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


url = f"https://drive.google.com/uc?id=1n0k_F7BYv3e8V6Ej4TmULayEX-SV0-XK"
output = "movies.pkl"
gdown.download(url, output, quiet=False)
df: pd.DataFrame = pd.read_pickle(output)


url = "https://drive.google.com/uc?id=1LmC39vrVrxM_AuBmoMoWTyUFPB7f8fE7"
output = "similarity.pkl"
gdown.download(url, output, quiet=False)
with open(output, "rb") as f:
    similarity = pickle.load(f)

app = Flask(__name__)
CORS(app)

trie = Trie()


def setupTrie():
    i = 0
    for _, row in df.iterrows():
        trie.insert(row["title"], row["movie_id"], i)
        i += 1


async def fetch(currId, headers, delay: float = 0):
    url = f"https://api.themoviedb.org/3/movie/{currId}?language=en-US"
    await asyncio.sleep(delay)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


async def fetch_posters(movie_ids):
    tasks = [fetch(_id, headers) for _id in movie_ids]
    responses = await asyncio.gather(*tasks)

    return [response for response in responses]


@app.route("/recommend", methods=["GET"])
def recommend():
    """Gives the n number of movies similar to the current movie

    Args:
        movie (str): Current Movie
        n (int, optional): The number of movie recommendations needed. Defaults to 5.
    """
    movie = request.args.get("movie")
    n: int = 5
    if not movie:
        return ""

    movie = movie.strip()

    indexes = trie.search(movie)
    if not indexes[1]:
        return []

    movie_index: int = indexes[1][0]
    distances = tuple(enumerate(similarity[movie_index]))
    distances = list(sorted(distances, reverse=True, key=lambda x: x[1]))
    nth_nearest = distances[1 : n + 1]

    data = []
    movie_ids = []
    for index, score in nth_nearest:
        row = df.iloc[index]
        data.append((row["title"], int(row["movie_id"])))
        movie_ids.append(int(row["movie_id"]))

    return jsonify(data)


@app.route("/get-movies", methods=["GET"])
def get_movies():
    inputStr: str | None = request.args.get("movie")
    if not inputStr:
        return ""

    inputStr = inputStr.strip().title()
    print(inputStr)
    indexes = trie.starts_with(inputStr)[1]

    df_filtered = df.iloc[indexes]["title"]
    # print(df_filtered)

    return jsonify(df_filtered.tolist())


if __name__ == "__main__":
    setupTrie()
    app.run(debug=False)