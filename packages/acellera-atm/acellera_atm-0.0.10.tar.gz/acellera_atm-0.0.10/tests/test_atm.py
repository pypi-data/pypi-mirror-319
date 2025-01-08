import shutil
import pytest
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skipping in CI")
def _test_structprep(tmp_path):
    from atm.rbfe_structprep import rbfe_structprep

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07"), os.path.join(tmp_path, "QB_A08_A07")
    )
    rbfe_structprep(os.path.join(tmp_path, "QB_A08_A07", "QB_A08_A07_asyncre.yaml"))


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skipping in CI")
def _test_explicit_sync(tmp_path):
    from atm.rbfe_production import rbfe_production

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07_completed"),
        os.path.join(tmp_path, "QB_A08_A07_completed"),
    )
    rbfe_production(
        os.path.join(tmp_path, "QB_A08_A07_completed", "QB_A08_A07_asyncre.yaml")
    )
