from compose_viz.models.device import Device


def test_device_init_normal() -> None:
    try:
        d = Device(host_path="/dev/ttyUSB0", container_path="/dev/ttyUSB1")

        assert d.host_path == "/dev/ttyUSB0"
        assert d.container_path == "/dev/ttyUSB1"
    except Exception as e:
        assert False, e


def test_device_with_cgroup_permissions() -> None:
    try:
        d = Device(host_path="/dev/sda1", container_path="/dev/xvda", cgroup_permissions="rwm")

        assert d.host_path == "/dev/sda1"
        assert d.container_path == "/dev/xvda"
        assert d.cgroup_permissions == "rwm"
    except Exception as e:
        assert False, e
