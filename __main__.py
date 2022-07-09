from flask import Flask
import ghhops_server as hs
import requests
import json
import urllib3
import argparse
from main import configs


def finish_conversion(f):
    def wrapper(*arg, **kwargs):
        return list(f(*arg, **kwargs))

    return wrapper


@finish_conversion
def pointlist_to_array(pts):
    for pt in pts:
        yield [pt.X, pt.Y, pt.Z]


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
        return json.dumps(r.json())


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
        return r.json()


@hops.component(
    "/osm_create_site",
    name='Get Osm Site',
    nickname='GetOsm',
    description="Initialize new section by its name on OpenStreetMap",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("name", "name", "name")

    ],
    outputs=[
        hs.HopsString("id", "id", "site id"),
    ],
)
async def osm_create_site(run, name):
    if run:
        r = requests.get(main_url + 'osm/site/' + name, verify=False)
        return r.json()


@hops.component(
    "/osm_site_from_coords",
    name='Get Osm Site from coords',
    nickname='GetOsmFromCrd',
    description="Initialize a new area by its coordinates on the OpenStreetMap",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsPoint(nickname="pts", name="points", desc="rhino points as list", access=hs.HopsParamAccess.LIST)

    ],
    outputs=[
        hs.HopsString("id", "id", "site id"),
    ],
)
async def osm_site_from_coords(run, pts):

    if run:
        num_pts = pointlist_to_array(pts)
        r = requests.post(main_url + 'osm/site/from_coords/', data=json.dumps({'kwargs': num_pts}), verify=False)
        return r.json()


@hops.component(
    "/osm_site_from_json",
    name='Get Osm Site from json',
    nickname='GetOsmFromJson',
    description="Initialize a new site by json string with coordinates on OpenStreetMap",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString(nickname="json", name="json_string_data", desc="json string")

    ],
    outputs=[
        hs.HopsString("id", "id", "site id"),
    ],
)
async def osm_site_from_json(run, string):
    if run:
        num_pts = '{"kwargs": '+string+'}'
        print(num_pts)
        r = requests.post(main_url + 'osm/site/from_coords/', data=num_pts, verify=False)
        return r.json()


@hops.component(
    "/site_list",
    name='List of saved Sites',
    nickname="SiteList",
    description="List of available saved territories",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),

    ],
    outputs=[
        hs.HopsString("sites", "sites", "saved sites"),
    ],
)
async def slist(run):
    if run:
        r = requests.get(main_url + 'osm/site_list/', verify=False)
        return r.json()


@hops.component(
    "/get_attribute",
    name="Get Site attribute",
    nickname="GetSiteAttr",
    description="Get attribute of Site object by id and name",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("id", "id", desc="Site object ID"),
        hs.HopsString("attr", "attr", desc="attribute name")

    ],
    outputs=[
        hs.HopsString("out", "out", "outputs", access=hs.HopsParamAccess.ITEM),
    ],
)
async def req_get_attr(run, site_id, attr):
    if run:
        r = requests.get(main_url + f"osm/site/{site_id}/{attr}", verify=False)
        return json.dumps(r.json())


@hops.component(
    "/get_method",
    name="Get Site method",
    nickname="GetSiteMethod",
    description="Call Site object method by id, method name and user arguments",
    inputs=[
        hs.HopsBoolean("run", "run", "run"),
        hs.HopsString("id", "id", desc="Site object ID"),
        hs.HopsString("name", "name", desc="METHOD NAME"),
        hs.HopsString("data", "data", desc="Custom arguments in the form of a dictionary", optional=True)

    ],
    outputs=[
        hs.HopsString("out", "out", "outputs", access=hs.HopsParamAccess.ITEM),
    ],
)
async def req_post_met(run, site_id, name, data):
    if run:
        r = requests.post(main_url + f"osm/site/{site_id}/{name}", data, verify=False)

        return json.dumps(r.json())


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
