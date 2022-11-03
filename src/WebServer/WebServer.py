from typing import Optional
import logging

from flask import Flask
from flask_restful import Api

from .exceptions import ResourceIsBusyException
from .routes import main_page, Page


class WebServer:
    app = Flask(__name__)

    def __init__(self, *, port: int, debug: bool):
        self.port = port
        self.debug = debug

        self.map = {}

        self.api = Api(self.app)
        self.add_web_endpoint_as_class(main_page.MainPage("/", "main", ['GET']))

    def add_resource(self, resource, path: Optional[str]):
        path = path if path else "/"

        if path in self.map.keys():
            raise ResourceIsBusyException.ResourceIsBusyException(path, "The path is already taken by another resource")

        self.api.add_resource(resource, path)
        self.__add_resource_to_map(path, resource)

    def add_web_endpoint(self, *, endpoint, name, handler, methods):
        if endpoint in self.map.keys():
            raise ResourceIsBusyException.ResourceIsBusyException(endpoint,
                                                                  "The path is already taken by another resource")

        self.__add_resource_to_map(endpoint, handler)
        self.app.add_url_rule(endpoint, name, handler, methods=methods)

    def add_web_endpoint_as_class(self, endpoint: Page):
        if endpoint.route in self.map.keys():
            raise ResourceIsBusyException.ResourceIsBusyException(endpoint.route,
                                                                  "The path is already taken by another resource")
        self.__add_resource_to_map(endpoint.route, endpoint.handler)

        self.app.add_url_rule(endpoint.route, endpoint.name, endpoint.handler, methods=endpoint.methods)

    def __add_resource_to_map(self, path, resource):
        self.map |= {path: resource}
        logging.info(f"{resource} was added to path {path if path else '/'}")

    def run(self) -> None:
        self.app.run(port=self.port, debug=self.debug)
