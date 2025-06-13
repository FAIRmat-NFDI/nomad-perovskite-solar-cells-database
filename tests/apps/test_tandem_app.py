def test_importing_app():
    # This will raise an exception if pydantic model validation fails for the app
    from perovskite_solar_cell_database.apps.tandem_app import (  # type: ignore
        tandem_app,  # noqa: F401
    )
