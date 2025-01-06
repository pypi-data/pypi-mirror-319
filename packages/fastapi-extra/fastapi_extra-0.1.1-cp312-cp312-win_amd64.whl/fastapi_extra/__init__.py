__version__ = "0.1.1"


def install(app) -> None:
    try:
        from fastapi_extra import routing as native_routing  # type: ignore
        
        native_routing.install(app)

    except ImportError:  # pragma: nocover
        pass
