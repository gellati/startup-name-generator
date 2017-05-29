from flask import Flask, render_template
from flask import jsonify
import json
import requests

from PIL import Image, ImageFont, ImageDraw

app = Flask(__name__)
app.debug = True


def getName():
    url="http://burgundy.io:8080"
    response=requests.get(url)
    data = response.content
    return data

# write text on the image
def writeImageText(imageData):
    imagePath='./static/images/'
    image = Image.open(imagePath+imageData[0]['img'])
    draw = ImageDraw.Draw(image)
    for i in range(len(imageData)):
        font = ImageFont.truetype("./static/fonts/SourceSansPro-Regular.ttf", imageData[i]['fontSize'])
        draw.text((imageData[i]['xcoord'], imageData[i]['ycoord']), imageData[i]['text'], font=font, fill=(0, 0, 0, 170))
    image.save(imagePath + "tt_" + imageData[0]['img'])


@app.route("/")
def mainpage():
    return render_template('landing_page.html')


@app.route("/loading")
def loading():
    return render_template('loading_page.html')


@app.route("/results")
def results():
    name = getName()
    # data on what should be written on the images and text position + font size
    articleData = [
        {'name': name, 'img': 'newspaper.jpg', 'text': name.title(), 'xcoord': 30, 'ycoord': 620, 'fontSize': 80},
        {'name': name, 'img': 'newspaper.jpg', 'text': 'gets 3 million $ funding', 'xcoord': 30, 'ycoord': 720, 'fontSize': 50}
    ]
    businesscardData = [
        {'name': name, 'img': 'business_card.jpg', 'text': name.capitalize(), 'xcoord': 150, 'ycoord': 120, 'fontSize': 50},
        {'name': name, 'img': 'business_card.jpg', 'text': 'Y Combinator', 'xcoord': 150, 'ycoord': 190, 'fontSize': 25},
        {'name': name, 'img': 'business_card.jpg', 'text': 'Batch 137', 'xcoord': 150, 'ycoord': 220, 'fontSize': 25}
    ]

    tabletData = [
        {'name': name, 'img': 'tabletphone.jpg', 'text': name.capitalize(), 'xcoord': 130, 'ycoord': 70, 'fontSize': 20},
        {'name': name, 'img': 'tabletphone.jpg', 'text': name.capitalize(), 'xcoord': 302, 'ycoord': 145, 'fontSize': 10}
    ]

    writeImageText(articleData)
    writeImageText(businesscardData)
    writeImageText(tabletData)
    return render_template('show_results.html', name=name)


if __name__ == "__main__":
    app.run(threaded=True)
