from flask import Flask, render_template
from flask import jsonify
from NameRnn import *
import json
import requests

from PIL import Image, ImageFont, ImageDraw


app = Flask(__name__)
app.debug = True
nrn = NameRnn()

def getName():
    url="http://burgundy.io:8080"
    response=requests.get(url)
    data = response.content
#    data = json.loads(response.content)
    return data

# TODO: not working yet
def writeImageText(image, text, xcoord, ycoord ):
    font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 25)
#    img = Image.new("RGBA", (200,200), (120,20,20))
    draw = ImageDraw.Draw(img)
    draw.text((0,0), "This is a test", (255,255,0), font=font)
    draw = ImageDraw.Draw(image)
    img.save("a-")



@app.route("/")
def mainpage():
    entries = nrn.get(5)
    print entries
    return render_template('landing_page.html')

@app.route("/loading")
def loading():
    return render_template('loading_page.html')

@app.route("/results")
def results():
    name = getName()
    article_text =  "gets 3 million $ funding"
    businesscard_text = "Best in what in class"
    return render_template('show_results.html', name=name)

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
