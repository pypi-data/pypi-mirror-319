from tcpb_trio import TCPBClient
import trio

from contextlib import asynccontextmanager
from tempfile import TemporaryDirectory
from random import randrange
from functools import partial
import shutil
from os import environ


GRAIN_SWORKER_CONFIG = dict()


@asynccontextmanager
async def grain_context(host, port):
    async with TCPBClient(host, port) as tc:
        yield tc


@asynccontextmanager
async def grain_run_sworker():
    with TemporaryDirectory(prefix="tcserver") as tempd:
        async with trio.open_nursery() as _n:
            host, port = trio.socket.gethostname(), randrange(10000, 65536)
            cmd = ["terachem", "-s", str(port)]
            if cli_args := environ.get("TCGRAIN_CLI_ARGS", ""):
                cmd.extend(cli_args.split())
            tcs = await _n.start(partial(trio.run_process, cmd, cwd=tempd))
            print("Waiting for TeraChem server to start...")
            await service_check(host, port)
            try:
                yield dict(
                    name=f"TCPB@{host}:{port}:g={environ.get('CUDA_VISIBLE_DEVICES', 'all')}",
                    host=host,
                    port=port,
                )
            finally:
                if environ.get("TCGRAIN_DEBUG_KEEPDIR", ""):
                    shutil.copytree(tempd, f"{tempd}-saved")
            tcs.terminate()


async def service_check(host, port):
    while True:
        await trio.sleep(1)
        try:
            async with TCPBClient(host, port) as tc:
                while True:
                    if await tc.is_available():
                        return
                    await trio.sleep(1)
        except:
            pass
