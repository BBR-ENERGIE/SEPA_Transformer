from bs4 import BeautifulSoup
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
            soup = BeautifulSoup(f, "xml")
            if soup.LclInstrm is not None:
                soup.LclInstrm.decompose()
            if soup.SeqTp is not None:
                soup.SeqTp.decompose()
            if soup.CtgyPurp is not None:
                for tag in soup.find_all("CtgyPurp"):
                    tag.decompose()
            if soup.PmtInf.find("PmtTpInf", recursive=False) is None:
                pmttpinf = soup.new_tag("PmtTpInf")
                instrprty = soup.new_tag("InstrPrty")
                instrprty.append("NORM")
                svclvl = soup.new_tag("SvcLvl")
                cd = soup.new_tag("Cd")
                cd.append("SEPA")
                svclvl.append(cd)
                pmttpinf.append(instrprty)
                pmttpinf.append(svclvl)

                soup.PmtInf.find("CtrlSum", recursive=False).insert_after(pmttpinf)

            with open(f"{path}/ok{file.filename}", "w") as fp:
                fp.write(str(soup))
        return send_from_directory(path, f"ok{file.filename}", as_attachment=True)
    return render_template("index.html")
