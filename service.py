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
    return render_template('show_entries.html', entries=entries)

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
    app.run()
