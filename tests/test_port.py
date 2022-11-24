from compose_viz.models.port import Port, Protocol


def test_port_init_normal() -> None:
    try:
        p = Port(host_port="8080", container_port="80")

        assert p.host_port == "8080"
        assert p.container_port == "80"
        assert p.protocol == Protocol.any
    except Exception as e:
        assert False, e

def test_port_with_unspecify_host() -> None:
    try:
        p = Port(host_port="", container_port="8080")
        assert p.host_port == ""
        assert p.container_port == "8080"
    except Exception as e:
        assert False, e

def test_port_with_protocol() -> None:
    try:
        p = Port(host_port="8080", container_port="80", protocol=Protocol.udp)

        assert p.host_port == "8080"
        assert p.container_port == "80"
        assert p.protocol == Protocol.udp
    except Exception as e:
        assert False, e
