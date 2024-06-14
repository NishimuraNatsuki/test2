from flask import Flask, render_template, url_for
import generate
import voicevox as v

app = Flask(__name__, static_folder="./static/")

g = generate.markov('txt/melos.txt')
g.wakachi()


@app.route('/', methods=["GET"])
def top():
    return render_template('index.html')

@app.route("/play", methods=["GET"])
def play():
    g.makelines()
    return render_template("index.html", lines = g.lines, new_lines = g.new_lines)

@app.route("/reset", methods=["GET"])
def reset():
    g.reset()
    return render_template("index.html", lines = g.lines, new_lines = g.new_lines)

@app.route("/voice", methods=["GET"])
def voice():
    v.text_to_voice(g.lines+g.new_lines)
    return render_template("index.html",lines = g.lines, new_lines = g.new_lines)


if __name__ == '__main__':
    app.run(debug=True)