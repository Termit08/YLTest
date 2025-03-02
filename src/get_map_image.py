import requests
# from PIL import Image
# from io import BytesIO


map_api_server = "https://static-maps.yandex.ru/1.x/"
map_apikey = "55515925-9197-4295-b309-a9fe09499027"


def get_map_image(longitude, lattitude, scale):

    map_params = {
        # "ll": ",".join([longitude, lattitude]),
        "ll": ",".join([lattitude, longitude]),
        "z": scale,
        "apikey": map_apikey,
        "size": "601,421",
        "l": "map",
    }

    response = requests.get(map_api_server, params=map_params)    

    if response.status_code == 200:
        with open("data/map.png", "wb") as file:
            file.write(response.content)
        return response.status_code, "data/map.png"
    else:
        return response.status_code, response.content

