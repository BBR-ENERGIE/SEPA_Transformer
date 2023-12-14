from flask import Flask, request, redirect, render_template, send_from_directory
from bs4 import BeautifulSoup

app = Flask(__name__)
path = "uploads"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.files:
        file = request.files["virement"]
        file.save(f"{path}/{file.filename}")
        with open(f"{path}/{file.filename}") as f:
            soup = BeautifulSoup(f, 'xml')
            if soup.LclInstrm is not None:
                soup.LclInstrm.decompose()
            if soup.SeqTp is not None:
                soup.SeqTp.decompose()

            with open(f"{path}/ok{file.filename}", "w") as fp:
                fp.write(str(soup.prettify()))
        return send_from_directory(path, f"ok{file.filename}", as_attachment=True)
    return render_template("index.html")
