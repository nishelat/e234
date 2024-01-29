import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import random
import requests
from io import BytesIO
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
locations = ["Great Wall of China, China",
				"Eiffel Tower, France",
				"Taj Mahal, India",
				"Grand Canyon, USA",
				"Colosseum, Italy",
				"Serengeti National Park, Tanzania",
				"Great Barrier Reef, Australia",
				"Pyramids of Giza, Egypt",
				"Stonehenge, England",
				"Santorini, Greece",
				"Yellowstone National Park, USA",
				"Angkor Wat, Cambodia",
				"Bali, Indonesia",
				"Petra, Jordan",
				"Tokyo, Japan",
				"Niagara Falls, Canada",
				"Dubai, United Arab Emirates",
				"Banff National Park, Canada",
				"Galapagos Islands, Ecuador",
				"Mount Everest, Nepal"]
random.shuffle(locations)

location = locations[0]
print(location)

client = OpenAI()
response = client.images.generate(
  model="dall-e-3",
  prompt="Photograph clearly depicting " + location,
  size="1024x1024",
  quality="standard",
)
artUrl = response.data[0].url

maxWidth = 600
maxHeight = 448
borderThickness = 20

blankPostcard = Image.open("postcard.png").resize((maxWidth, maxHeight))

# artUrl = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-jMGFhEBt8ibshT5VHeK7Lsfv/user-vjlZUJXEQ4swDFxVCuQog73V/img-6FBmNBmEqzJyVYxuJe6ThuAB.png?st=2024-01-29T19%3A39%3A32Z&se=2024-01-29T21%3A39%3A32Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-29T01%3A35%3A55Z&ske=2024-01-30T01%3A35%3A55Z&sks=b&skv=2021-08-06&sig=2XO2IkWYs2xJ3QvfYvrVzi4UGBZ6fJLOuksfuiGKApo%3D";
artResponse = requests.get(artUrl)
art = Image.open(BytesIO(artResponse.content)).resize((maxWidth, maxWidth)).crop((borderThickness, borderThickness, maxWidth - borderThickness, maxHeight - borderThickness))

draw = ImageDraw.Draw(art)
draw.text((borderThickness, borderThickness), location, font = font24, fill = "#ffffff")

blankPostcard.paste(art, (borderThickness, borderThickness))
blankPostcard.show()