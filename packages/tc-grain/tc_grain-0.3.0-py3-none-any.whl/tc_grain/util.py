import subprocess
from os import environ
import argparse
import math
from socket import gethostname


def tcpb_spawn():
    argp = argparse.ArgumentParser(
        epilog="Start TCPB Grain specialized worker based on current machine's GPU resources"
    )
    argp.add_argument(
        "-n",
        "--ngpu",
        type=int,
        default=math.inf,
        help="Maximum number of GPUs to take (default: all of the available ones)",
    )
    argp.add_argument(
        "-m",
        type=int,
        default=1,
        help="Number of TeraChem processes per GPU (default: 1)",
    )
    argp.add_argument(
        "--foreground",
        action="store_true",
        help="Run in foreground",
    )
    args = argp.parse_args()
    _tcpb_spawn(args)


def _tcpb_spawn(args):
    def _run(cmd):
        return subprocess.run(
            cmd, shell=True, check=True, stdout=subprocess.PIPE
        ).stdout.decode()

    if 'CUDA_VISIBLE_DEVICES' in environ:
        print(f"Using CUDA_VISIBLE_DEVICES={environ['CUDA_VISIBLE_DEVICES']}")
        gl = environ['CUDA_VISIBLE_DEVICES'].split(",")
    else:
        total = int(_run("nvidia-smi -L | wc -l").strip())
        nv_smi = iter(_run("nvidia-smi").split("\n"))
        for gl in nv_smi:
            if "Processes" in gl:
                break
        next(nv_smi)
        next(nv_smi)
        next(nv_smi)
        occupied = set()
        for gl in nv_smi:
            if "---" in gl or "No" in gl:
                break
            occupied.add(int(gl.split()[1]))

        gl = list(set(range(total)) - occupied)
        gl = gl[: min(len(gl), args.ngpu)]
        print(
            f"{total-len(occupied)} out of {total} GPU(s) are available; taking {len(gl)} GPU(s)"
        )

    host = gethostname()
    procs = []
    for i in gl:
        for j in range(args.m):
            tmplog = f"tcpb-grain-{host}-device{i}-{j}.log"
            p = subprocess.Popen(
                f"grain up > {tmplog} 2>&1 && rm -f {tmplog}",
                shell=True,
                env=environ | dict(CUDA_VISIBLE_DEVICES=str(i)),
                start_new_session=not args.foreground,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            procs.append(p)

    if args.foreground:
        for p in procs:
            p.wait()
