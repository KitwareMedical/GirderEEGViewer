from .core import EEGApp


def main(server=None, **kwargs):
    app = EEGApp(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
