import requests
from PIL import Image, ImageDraw


map_api_server = "https://static-maps.yandex.ru/1.x/"
map_apikey = "55515925-9197-4295-b309-a9fe09499027"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/?"
geocoder_apikey = "8013b162-6b42-4997-9691-77b7074026e0"


def get_map_image(longitude, lattitude, scale, theme):
    try:
        map_params = {
            # "ll": ",".join([longitude, lattitude]),
            "ll": ",".join([str(longitude), str(lattitude)]),
            "z": scale,
            "theme": theme,
            "apikey": map_apikey,
            "size": "601,421",
            "l": "map",
        }

        response = requests.get(map_api_server, params=map_params)    
    except Exception as e:
        return 500, e
    
    if response.status_code == 200:
        with open("data/map.png", "wb") as file:
            file.write(response.content)
        return response.status_code, "data/map.png"
    else:
        return response.status_code, response.content


def get_toponym_ll(geocode):
    geocoder_params = {
    "apikey": geocoder_apikey,
    "geocode": geocode,
    "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates.split(" ")

def draw_point(image):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    center_x = width // 2
    center_y = height // 2
    point_radius = 4
    
    draw.ellipse((center_x - point_radius, center_y - point_radius, 
        center_x + point_radius, center_y + point_radius),
        fill="red")

    return image

