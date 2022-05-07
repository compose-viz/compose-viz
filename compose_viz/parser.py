from compose_viz.compose import Compose


class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # validate input file using `docker-compose config -q sys.argv[1]` first
        raise NotImplementedError
