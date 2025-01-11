import shutil
import os


curr_dir = os.path.dirname(os.path.abspath(__file__))


def _test_structprep(tmp_path):
    from atm.rbfe_structprep import rbfe_structprep

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07"), os.path.join(tmp_path, "QB_A08_A07")
    )
    rbfe_structprep(os.path.join(tmp_path, "QB_A08_A07", "QB_A08_A07_asyncre.yaml"))


def _test_production(tmp_path):
    from atm.rbfe_production import rbfe_production

    shutil.copytree(
        os.path.join(curr_dir, "QB_A08_A07_completed"),
        os.path.join(tmp_path, "QB_A08_A07_completed"),
    )
    rbfe_production(
        os.path.join(tmp_path, "QB_A08_A07_completed", "QB_A08_A07_asyncre.yaml")
    )


def _test_uwham_analysis(tmp_path):
    from atm.uwham import calculate_uwham

    shutil.copytree(
        os.path.join(curr_dir, "TYK2_A02_A09_r0_1"),
        os.path.join(tmp_path, "TYK2_A02_A09_r0_1"),
    )

    run_dir = os.path.join(tmp_path, "TYK2_A02_A09_r0_1")

    ddG, ddG_std, _, _, _ = calculate_uwham(run_dir, "QB_A02_A09", 70, 1000000)

    expected_ddG = -1.0582613105156682
    expected_ddG_std = 0.19669046441083107
    assert abs(ddG - expected_ddG) < 1e-8
    assert abs(ddG_std - expected_ddG_std) < 1e-8
