from flask import Flask
import ghhops_server as hs
import requests
import json
import urllib3
import argparse
from main import configs

import ast
urllib3.disable_warnings()

app = Flask(__name__)
hops = hs.Hops(app)

main_url = f'http://localhost:{configs.main.port}/'
@hops.component(
    "/GET",
    name="GET",
    description="GET request",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),


        hs.HopsString("name", "name", "name"),
    ],
    outputs=[
        hs.HopsString("out", "out", "outputs", access=hs.HopsParamAccess.ITEM),
    ],
)
async def req_get(run, name):
    if run:
        r = requests.get(main_url + name, verify=False)
        return r.json()


@hops.component(
    "/POST",
    name="POST",
    description="POST request",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),

        hs.HopsString("name", "name", "name"),
        hs.HopsString("data", "data", "data")
    ],
    outputs=[
        hs.HopsString("out", "out", "outputs"),
    ],
)
async def req_post(run, name, data):
    if run:
        r = requests.post(main_url + name, data, verify=False)
        return json.dumps(r.json())


@hops.component(
    "/PUT",
    name="PUT",
    description="PUT request",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("name", "name", "name"),
        hs.HopsString("data", "data", "data")
    ],
    outputs=[
        hs.HopsString("out", "out", "outputs"),
    ],
)
async def req_put(run, name, data):
    if run:
        r = requests.put(main_url + name, data, verify=False)
        return json.dumps(r.json())



@hops.component(
    "/osm_create_site",
    name='Get Osm Site',
    nickname='GetOsm',
    description="Инициализировать новый участок по его имени на OpenStreetMap",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("name", "name", "name")

    ],
    outputs=[
        hs.HopsString("id", "id", "site id"),
    ],
)
async def create_site(run, name):
    if run:
        r = requests.get(main_url + 'osm/site/' + name, verify=False)
        return r.json()


@hops.component(
    "/site_list",
    name='List of saved Sites',
    nickname="SiteList",
    description="Список доступных сохраненных территорий",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),

    ],
    outputs=[
        hs.HopsString("sites", "sites", "saved sites"),
    ],
)
async def slist(run):
    if run:
        r = requests.get(main_url + 'osm/site_list/' ,verify=False)
        return r.json()

@hops.component(
    "/get_attribute",
    name="Get Site attribute",
    nickname="GetSiteAttr",
    description="Получить атрибут объекта Site по id и имени",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("id", "id", desc="id объекта Site"),
        hs.HopsString("attr", "attr", desc="Имя атрибута")



    ],
    outputs=[
        hs.HopsString("out", "out", "outputs", access=hs.HopsParamAccess.ITEM),
    ],
)
async def req_get_attr(run, id, attr):
    if run:
        r = requests.get(main_url + f"osm/site/{id}/{attr}", verify=False)
        return r.json()


@hops.component(
    "/get_method",
    name="Get Site attribute",
    nickname="GetSiteMethod",
    description="Вызвать метод объекта Site по id, имени метода и пользовательским аргументам",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("id", "id", desc="id объекта Site"),
        hs.HopsString("name", "name", desc="Имя метода"),
        hs.HopsString("data", "data", desc="Пользовательские аргументы в виде словаря", optional=True)

    ],
    outputs=[
        hs.HopsString("out", "out", "outputs", access=hs.HopsParamAccess.ITEM),
    ],
)
async def req_post_met(run, id, name, data):
    if run:


        r = requests.post(main_url + f"osm/site/{id}/{name}", data, verify=False)

        return r.json()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Running gh hops server')
    parser.add_argument('-hs', '--host', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument('-d', '--debug', type=bool, default=True)

    args = parser.parse_args()
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
