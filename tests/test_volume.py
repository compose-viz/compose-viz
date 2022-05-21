from compose_viz.volume import Volume, VolumeType


def test_volume_init_normal() -> None:
    try:
        v = Volume(source="./foo", target="./bar")

        assert v.source == "./foo"
        assert v.target == "./bar"
        assert v.type == VolumeType.volume
    except Exception as e:
        assert False, e


def test_volume_with_type() -> None:
    try:
        v = Volume(source="./foo", target="./bar", type=VolumeType.bind)

        assert v.source == "./foo"
        assert v.target == "./bar"
        assert v.type == VolumeType.bind
    except Exception as e:
        assert False, e
