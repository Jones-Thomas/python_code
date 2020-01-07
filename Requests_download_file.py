import requests

url = "http://bestanimations.com/Books/girl-reading-book.gif#.XhUD2ACdpPA.link"
with open("D:\\Jones\\Python\\pycharm\\python_alert\\Girl_reading_gif.gif", "wb") as f:
    f.write(requests.get(url).content)

