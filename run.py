import os

import torch

from models import models
from src.dirnames import dirnames
from src.exceptions import AlreadyTrainedError
from src.run_preprocesses import get_args_and_config_file


def main():
    args, config = get_args_and_config_file()

    save_dir = args.config_file_name.replace(
        dirnames.configs, dirnames.results
    ).replace(".yaml", "")
    os.makedirs(save_dir, exist_ok=True)

    trained_file_path = os.path.join(save_dir, "trained.txt")
    if os.path.exists(trained_file_path):
        if args.overwrite:
            print(f"{args.config_file_name} is already trained, but overwriting it.")
            os.remove(trained_file_path)
        else:
            raise AlreadyTrainedError(args.config_file_name)

    cpu = torch.device("cpu")
    gpu = (
        torch.device(f"cuda:{args.device}")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )

    main_process(config=config, save_dir=save_dir, cpu=cpu, gpu=gpu)

    with open(os.path.join(save_dir, "trained.txt"), "w") as writer:
        pass
    return


def main_process(
    config: dict[str, dict],
    save_dir: str,
    cpu: torch.device,
    gpu: torch.device,
):
    model_params: dict = config["model_params"]
    model = models[model_params["name"]](**model_params, cpu=cpu, gpu=gpu, save_dir=save_dir)
    model.compute_area()


if __name__ == "__main__":
    main()
