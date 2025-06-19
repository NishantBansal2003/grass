import os
import grass.script as gs
import pytest


@pytest.fixture
def setup_session(tmp_path_factory, monkeypatch):
    """Creates a session with a mapset"""
    tmp_path = tmp_path_factory.mktemp("simple_dataset")
    location = "test_project"
    gs.core._create_location_xy(tmp_path, location)  # pylint: disable=protected-access
    with gs.setup.init(tmp_path / location, env=os.environ.copy()) as session:
        for key, value in session.env.items():
            monkeypatch.setenv(key, value)
        yield session


@pytest.fixture
def simple_dataset(setup_session):
    """Set up a GRASS session for the tests."""
    mapset = "test_1"
    project = "test_project"

    gs.run_command("g.region", rows=3, cols=3, env=setup_session.env)

    # Create Mock Mapsets and data in each
    gs.run_command(
        "g.mapset", project=project, mapset=mapset, flags="c", env=setup_session.env
    )

    # Create a raster in this mapset
    gs.mapcalc(f"raster_{mapset} = int(row())", env=setup_session.env)
    gs.run_command(
        "r.support",
        map=f"raster_{mapset}",
        title=f"Raster title {mapset}",
        env=setup_session.env,
    )

    # Create a vector in this mapset
    gs.run_command(
        "v.mkgrid",
        map=f"vector_{mapset}",
        grid=[10, 10],
        type="point",
        env=setup_session.env,
    )
    gs.run_command(
        "v.support",
        map=f"vector_{mapset}",
        map_name=f"Vector title {mapset}",
        env=setup_session.env,
    )

    yield setup_session
