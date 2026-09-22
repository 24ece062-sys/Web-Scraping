from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load CSV file
df = pd.read_csv("../imdb_top_250.csv")


# Home route
@app.route("/")
def home():
    return "IMDb Movie API is running!"


# Get all movies
@app.route("/api/movies")
def get_movies():
    movies = df.to_dict(orient="records")
    return jsonify(movies)


# Search movie by title
@app.route("/api/search")
def search_movie():

    query = request.args.get("title", "")

    result = df[
        df["Title"].str.contains(
            query,
            case=False,
            na=False
        )
    ]

    return jsonify(
        result.to_dict(orient="records")
    )


# Rating filter
@app.route("/api/rating")
def rating_filter():

    rating = request.args.get("rating", 0, type=float)

    result = df[df["Rating"] >= rating]

    return jsonify(
        result.to_dict(orient="records")
    )


# Statistics
@app.route("/api/stats")
def statistics():

    total_movies = len(df)

    average_rating = df["Rating"].mean()

    return jsonify({
        "total_movies": total_movies,
        "average_rating": round(average_rating, 2)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)