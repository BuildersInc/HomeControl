from WebServer import WebServer


if __name__ == '__main__':
    web_app = WebServer.WebServer(port=5005, debug=True)
    # web_app.add_web_endpoint("/", 'action', action, ['GET'])
    web_app.run()
