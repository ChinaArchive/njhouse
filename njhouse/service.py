# coding:utf-8

from flask import Flask
from sitepages import FlaskResponse

from .utils import njhouse_query

app = Flask(__name__)


@app.route("/")
@FlaskResponse.markdown
def index() -> str:
    return "# Welcome to the homepage!"


@app.route("/health")
@FlaskResponse.plain
def healthcheck() -> str:
    return "good"


@app.route("/query")
@FlaskResponse.json
def query_now():
    query = njhouse_query()
    return query.dict_all()


# @app.route("/query/<>")
# def query_(time1, time2):
#     return f"Hello, {time1}, {time2}!"


def run(host: str = "0.0.0.0", port: int = 41012, debug: bool = False):
    app.run(host=host, port=port, debug=debug)
