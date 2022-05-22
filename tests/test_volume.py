from compose_viz.volume import AccessMode, Volume, VolumeType


def test_volume_init_normal() -> None:
    try:
        v = Volume(source="./foo", target="./bar")

        assert v.source == "./foo"
        assert v.target == "./bar"
        assert v.type == VolumeType.volume
        assert v.access_mode == AccessMode.rw
    except Exception as e:
        assert False, e


def test_volume_with_type() -> None:
    try:
        v = Volume(source="./foo", target="./bar", type=VolumeType.bind)

        assert v.source == "./foo"
        assert v.target == "./bar"
        assert v.type == VolumeType.bind
        assert v.access_mode == AccessMode.rw
    except Exception as e:
        assert False, e


def test_volume_with_access_mode() -> None:
    try:
        v = Volume(source="./foo", target="./bar", access_mode=AccessMode.ro)

        assert v.source == "./foo"
        assert v.target == "./bar"
        assert v.type == VolumeType.volume
        assert v.access_mode == AccessMode.ro
    except Exception as e:
        assert False, e
