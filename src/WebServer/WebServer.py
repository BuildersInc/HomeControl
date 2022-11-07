from typing import Optional
import logging

from flask import Flask
from flask_restful import Api

from .exceptions import ResourceIsBusyException
from .routes import main_page


class WebServer:
    app = Flask(__name__)

    def __init__(self, *, port: int, debug: bool):
        self.port = port
        self.debug = debug

        self.map = []

        self.api = Api(self.app)
        self.add_web_endpoint_as_class(main_page.MainPage("/", "main", ['GET']))

    def add_resource(self, resource, path: Optional[str]):
        path = path if path else "/"

        if path in self.map:
            raise ResourceIsBusyException.ResourceIsBusyException(path, "The path is already taken by another resource")

        self.api.add_resource(resource, path)
        self.__add_resource_to_map(path)

    def add_web_endpoint(self, *, endpoint, name, handler, methods):
        if endpoint in self.map:
            raise ResourceIsBusyException.ResourceIsBusyException(endpoint,
                                                                  "The path is already taken by another resource")

        self.__add_resource_to_map(endpoint)
        self.app.add_url_rule(endpoint, name, handler, methods=methods)

    def add_web_endpoint_as_class(self, endpoint):
        if endpoint.route in self.map:
            raise ResourceIsBusyException.ResourceIsBusyException(endpoint.route,
                                                                  "The path is already taken by another resource")
        self.__add_resource_to_map(endpoint.route)

        self.app.add_url_rule(endpoint.route, endpoint.name, endpoint.handler, methods=endpoint.methods)

    def __add_resource_to_map(self, path: str) -> None:
        """
        Adds the path to a list in order to keep track of used
        endpoints

        Args:
            path: the url path to the API / APP endpoint

        Returns:
            None

        """
        self.map.append(path)
        logging.info(f"{path} was registered")

    def run(self) -> None:
        """
        Starts the Webserver Process

        CAUTION:
            Blocks everything after the run call until the Webserver is closed

        Returns:
            None

        """
        self.app.run(port=self.port, debug=self.debug)
