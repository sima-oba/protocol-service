from .server import create_server


def start_flask_server(config, host: str, port: int):
    server = create_server(config)
    server.run(host=host, port=port)


def start_gunicorn_server(config, host: str, port: int, workers: int):
    from .gunicorn import GunicornApplication

    server = create_server(config)
    options = {'bind': f'{host}:{port}', 'workers': workers}
    GunicornApplication(server, options).run()
