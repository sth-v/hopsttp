import os
from flask import Flask
import ghhops_server as hs
import requests
import json
import urllib3
import argparse

main_port = os.environ["TARGET_PORT"]
main_host = os.environ["TARGET_HOST"]
main_url = f'{main_host}:{main_port}/'

import ast
urllib3.disable_warnings()

app = Flask(__name__)
hops = hs.Hops(app)

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
def req_get(run, name):
    if run:
        print(main_url+name)
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
def req_post(run, name, data):
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
def req_put(run, name, data):
    if run:
        r = requests.put(main_url + name, data, verify=False)
        return json.dumps(r.json())


if __name__=="__main__":
    app.run(host=os.environ["HOPS_HOST"],
            port=int(os.environ["HOPS_PORT"]),
            debug=True
        )
