from .core import ViewerApp


def main(**kwargs) -> None:
    app = ViewerApp()
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
