from ruamel.yaml import YAML, YAMLError
from tap import Tap


class ArgumentParser(Tap):
    config_file_name: str
    device: int = -1
    overwrite: bool = False

    def configure(self):
        self.add_argument("--config_file_name", "-c")
        self.add_argument("--device", "-d")
        self.add_argument("--overwrite", "-overwrite")

def get_args_and_config_file():
    args = ArgumentParser(explicit_bool=True).parse_args()
    with open(args.config_file_name, "r") as file:
        try:
            config: dict[str, dict] = YAML(typ="safe").load(file)
        except YAMLError as exc:
            print(exc)
            quit()
    print(f"Start the process with {args.config_file_name}")
    return args, config
