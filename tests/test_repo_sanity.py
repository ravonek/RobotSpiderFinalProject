def test_repo_layout():
    # Very lightweight sanity check to ensure important paths exist.
    import os

    expected = [
        "README.md",
        "docs/abstract.md",
        "docs/hardware.md",
        "docs/architecture.md",
        "docs/gait.md",
        "docs/simulation.md",
        "docs/firmware.md",
        "firmware/pico/spider_firmware.py",
        "sim/isaac/spider_isaac_sim.py",
    ]
    for p in expected:
        assert os.path.exists(p), f"Missing: {p}"
