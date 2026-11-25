from flask import Flask, render_template, request
from database import filter_games, get_statistics, get_game_by_id

app = Flask(__name__)


@app.route("/")
def home():

    search = request.args.get("search", "")
    store = request.args.get("store", "")

    sort = request.args.get("sort", "")

    page = request.args.get("page", 1, type=int)

    games = filter_games(
        search=search,
        sort=sort,
        store=store,
        page=page,
        per_page=12
    )

    total, average, lowest, highest = get_statistics()

    return render_template(
        "index.html",
        games=games,
        total=total,
        average=average,
        lowest=lowest,
        highest=highest,
        search=search,
        sort=sort,
        store=store,
        page=page
    )


@app.route("/game/<int:game_id>")
def game_details(game_id):

    game = get_game_by_id(game_id)

    return render_template(
        "game.html",
        game=game
    )


if __name__ == "__main__":
    app.run(debug=True)