import sys
import os

import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import random
import requests
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)

datasetResponse = requests.get("https://api.artic.edu/api/v1/artworks/search?q=watercolor&size=100")
dataset = datasetResponse.json()["data"]
ids = []
for artworkOverview in dataset:
    ids.append(artworkOverview["id"])
random.shuffle(ids)

for artworkId in ids:
    artworkResponse = requests.get("https://api.artic.edu/api/v1/artworks/" + str(artworkId))
    imageId = artworkResponse.json()["data"]["image_id"]
    imageUrl = "https://www.artic.edu/iiif/2/" + imageId + "/full/600,/0/default.jpg"
    imageResponse = requests.get(imageUrl)
    image = Image.open(BytesIO(imageResponse.content)).resize((600, 448))
    image.show()
    time.sleep(10)