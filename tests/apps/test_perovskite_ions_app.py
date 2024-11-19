def test_importing_app():
    # This will raise an exception if pydantic model validation fails for the app
    from perovskite_solar_cell_database.apps.perovskite_ions_app import (  # type: ignore
        perovskite_ions_app,  # noqa: F401
    )
