import os
import re
from glob import glob

import torch
from tap import Tap

from src.utils import str2bool


class ArgumentParser(Tap):
    filename_key: str
    devices: list[int]
    is_check: bool = True
    is_gpu: bool = True
    overwrite: bool = False
    """If true, the result folder will be overwritten.
    If false(default), the process is skipped when the result already exists."""

    def configure(self):
        self.add_argument("--filename_key", "-c")
        self.add_argument("--devices", "-d", nargs="*")
        self.add_argument("--is_check", "-check", type=str2bool)
        self.add_argument("--is_gpu", "-gpu", type=str2bool)
        self.add_argument("--overwrite", '-overwrite', "-w")

def get_args():
    args = ArgumentParser(explicit_bool=True).parse_args()
    print_str = (
        f"filename_key: {args.filename_key}, "
        + f"devices: {args.devices}, "
        + f"is_check: {args.is_check}, "
        + f"is_gpu: {args.is_gpu}, "
        + f"overwrite: {args.overwrite}"
    )
    #print(print_str)
    if not torch.cuda.is_available():
        assert not args.is_gpu, "GPU is not available now."
        assert len(args.devices) == 1, ""
    return args

def search_config_files(args: ArgumentParser):
    filename_key = args.filename_key
    filename_end = "*.yaml"
    pattern_end = (
        r"(?<!(-|_)base)\.yaml"
    )
    configfiles = [
        path
        for path in glob(os.path.join("configs", "**", filename_end), recursive=True)
        if re.search(pattern_end, path) and re.search(rf"{filename_key}", path)
    ]
    assert len(configfiles) > 0, f'filenames = {", ".join(configfiles)}'
    print('Config file list:')
    for configfile in configfiles:
        print(configfile)
    if not args.is_check:
        return configfiles
    ans = input("Do you want to run run.py with these files? [y/n]" + os.linesep)
    if ans.lower() != "y":
        os._exit(0)
    return configfiles
