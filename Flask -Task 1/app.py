from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

def analyze_name(username):
    transformations = {
        "UPPERCASE": username.upper(),
        "REVERSED": "".join(reversed(username)),
        "VOWEL_COUNT": sum(1 for ch in username.lower() if ch in "aeiou"),
        "CHAR_COUNT": len(username),
        "PERSONALITY": "BOLD" if len(username) > 6 else "MINIMAL"
    }
    return transformations

@app.route("/")
def name_handler():
    user = request.args.get("user")

    if user is None:
        return render_template("name_view.html", status="EMPTY")

    result = analyze_name(user)

    return render_template(
        "name_view.html",
        status="OK",
        original=user,
        analysis=result,
        timestamp=datetime.now().strftime("%d %b %Y | %H:%M:%S")
    )

if __name__ == "__main__":
    app.run(debug=True)
