import signal
import subprocess
import sys
import time
import traceback
from multiprocessing import Manager, Pool
from queue import Queue

import torch

from src.exceptions import AlreadyTrainedError
from src.multi_run_preprocesses import (ArgumentParser, get_args,
                                        search_config_files)


def main():
    args = get_args()
    configfiles = search_config_files(args=args)
    run_parallel(args=args, configfiles=configfiles)


def run_parallel(args: ArgumentParser, configfiles: list[str]):
    m = Manager()
    queue = m.Queue()
    is_gpu = torch.cuda.is_available() and args.is_gpu

    # initialize the queue with the GPU ids
    for gpu_id, num in enumerate(args.devices):
        for _ in range(num):
            queue.put(gpu_id)

    commands = [
        f"python run.py -c {configfile}" + f" --overwrite {args.overwrite}"
        for configfile in configfiles
    ]
    print("Command list:")
    for command in commands:
        print(command)

    pool = Pool(processes=sum(args.devices))
    num_finished = 0
    time0 = time.time()

    signal.signal(signal.SIGTERM, sig_handler)
    try:
        for command in pool.imap_unordered(
            run_subprocess, [(queue, com, is_gpu) for com in commands]
        ):
            num_finished += 1
            time1 = time.time()
            print(
                f"The process finished: {command} [{num_finished}/{len(commands)}]"
                #+ f" ({time1-time0:.2e}s)"
            )
        pool.close()
        pool.join()
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print("Process pool is closing...")
        pool.close()
        pool.terminate()
        print("Process pool closed.")
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


def run_subprocess(args: tuple[Queue, str, bool]):
    queue, command, is_gpu = args
    gpu_id = queue.get()
    with (
        subprocess.Popen(f"{command} -d {gpu_id}", shell=True)
        if is_gpu
        else subprocess.Popen(command, shell=True)
    ) as process:
        try:
            process.wait()
        except AlreadyTrainedError:
            splitted_command = command.split(sep=" ")
            filename = splitted_command[splitted_command.index("-c") + 1]
            print(f"AlreadyTrainedError: {filename} is already trained.")
        except KeyboardInterrupt:
            splitted_command = command.split(sep=" ")
            filename = splitted_command[splitted_command.index("-c") + 1]
            print(f"KeyboardInterrupt: {filename}")
        except Exception as exc:
            splitted_command = command.split(sep=" ")
            filename = splitted_command[splitted_command.index("-c") + 1]
            print(traceback.format_exc(), end="")
            print(f": {filename}")
        finally:
            queue.put(gpu_id)
    return command


def sig_handler(signum, frame):
    """
    ref:
    https://qiita.com/qualitia_cdev/items/f536002791671c6238e3
    """
    print("multi-run.py is terminated by KeyboardInterrupt or kill")
    sys.exit(1)


if __name__ == "__main__":
    main()
