from server.app import create_app

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5003


def main():
    app = create_app()
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)


if __name__ == '__main__':
    main()
