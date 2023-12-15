from flask import Flask, request, render_template, send_from_directory
import regex

app = Flask(__name__)
path = "uploads"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.files:
        file = request.files["virement"]
        file.save(f"{path}/{file.filename}")
        with open(f"{path}/{file.filename}") as f:
            strfile = f.read()
            strfile = regex.sub(r"\n\t*<LclInstrm>\X*<\/LclInstrm>", "", strfile)
            strfile = regex.sub(r"\n\t*<SeqTp>\X*<\/SeqTp>", "", strfile)

            with open(f"{path}/ok{file.filename}", "w") as fp:
                fp.write(strfile)
        return send_from_directory(path, f"ok{file.filename}", as_attachment=True)
    return render_template("index.html")
