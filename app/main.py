from flask import Flask, request
from os import listdir
from random import shuffle, randint
from PIL import Image
from flask import send_from_directory
from secrets import token_urlsafe
from configparser import ConfigParser

config = ConfigParser()
config.read("server.cfg")

server_url = config["GENERAL"]["server"]
token = config["GENERAL"]["token"]

# tarot logic goes here
def get_reading(amount):
        # cards in resources folder
        cards = listdir("app/resources/tarot")
        # magic shuffling
        shuffle(cards)
        reading = []
        for i in range(amount):
            # how 2 reverse a queue
            reading.append(cards.pop())

        # return the tempfile with the image
        return(make_image(reading))

def make_image(reading):
        reading_image = Image.new('RGB', (250 * len(reading), 429))

        for i in range(len(reading)):
            # chance for flipped card
            if randint(0,10) == 0:
                card_image = Image.open("app/resources/tarot/" + reading[i])
                image_flipped = card_image.transpose(Image.FLIP_TOP_BOTTOM)
                reading_image.paste(im=image_flipped, box=(250 * i, 0))
            #normal card
            else:
                reading_image.paste(im=Image.open("app/resources/tarot/" + reading[i]), box=(250 * i, 0))

        image_filename = "i/" + token_urlsafe(4) + ".jpg"
        reading_image.save("app/" + image_filename)
        return(server_url + image_filename)

# main router
app = Flask(__name__, static_url_path="")
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST' and request.form.get("token") == token:
        try:
            amount = int(request.form.get("amount"))
            return get_reading(amount) + "\n"
        except ValueError:
            return "Not a number!\n"
    else:
        return("Status OK")

@app.route('/i/<path:path>')
def serve_image(path):
    return send_from_directory('i', path)

if __name__ == "__main__":
    app.run(debug=True)