from flask import Flask, render_template
from flask import jsonify
from NameRnn import *
import json

app = Flask(__name__)
app.debug = True
nrn = NameRnn()

@app.route("/")
def mainpage():
    entries = nrn.get(5)
    print entries
    return render_template('landing_page.html', entries=entries)

@app.route("/results")
def results():
    results = {'name': 'Nimi2'}
    return render_template('show_results.html', name=results)

#def checkin():
#    functionality = 'not functional'
#    if nrn is not None:
#        functionality = "functional and healthy"
#    return jsonify(functionality=functionality)

@app.route("/get/<int:num>")
def get(num):
    names = nrn.get(num)
    return jsonify(names=names)




if __name__ == "__main__":
    app.run(threaded=True)
