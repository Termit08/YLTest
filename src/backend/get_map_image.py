import requests

from PIL import Image
from io import BytesIO


map_api_server = "https://static-maps.yandex.ru/1.x/"
map_apikey = "55515925-9197-4295-b309-a9fe09499027"


def get_map_image(longitude, lattitude, scale):

    map_params = {
        "ll": ",".join([longitude, lattitude]),
        "z": scale,
        "apikey": map_apikey,
        "size": "601,621",
        "l": "map",
    }

    response = requests.get(map_api_server, params=map_params)

    if response:
        img_data = response.content
        map_image = Image.open(BytesIO(img_data))
    else:
        return None
    return map_image
