#!/usr/bin/env python3

import rclone # local library using RPC calls, not PyPi!
import logging
import tomllib
from pathlib import Path
from pydantic import BaseModel
from sys import argv as sys_argv

script_name = str(Path(sys_argv[0]).stem)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(script_name)

class Remote(BaseModel):
    gives: list[str] | None
    receives: list[str] | None
    base_path: str | None

class Config(BaseModel):
    remotes: dict[str, Remote]

def replicate(config: Config):
    for src_remote, src_action in config.remotes.items():
        if not src_action.gives: # remote doesn't backup anything
            continue

        for source in src_action.gives:
            for dst_remote in config.remotes.keys() - src_remote:
                dst_action: Remote = config.remotes[dst_remote]

                if dst_action.receives and source in dst_action.receives:
                    log.info(f"replicating '{source}' from {src_remote} to {dst_remote}")
                    # replicate_sync(sync, remote, otherRemote)

# def replicate_appdata(
#         rc: rclone.Rclone,
#         server: str,
#         srcRemote: Remote,
#         dstRemote: Remote):

#     if SyncType.APPDATA not in dstRemote.allowed_syncs:
#         log.info(f'appdata sync not allowed for {dstRemote}')
#         return

#     appdata_path = f'appdata-{server}'

#     log.info('replicating appdata...')
#     rc.rpc('sync/sync', {
#         'srcFs': srcRemote.append_path(appdata_path),
#         'dstFs': dstRemote.append_path(appdata_path),
#         '_async': True
#     })

def main():
    log.info('loading librclone shared library...')
    rc = rclone.Rclone('/home/joao/sources/personal-server-stack/scripts/librclone.so')

    try:
        with open (
            '/home/joao/sources/personal-server-stack/scripts/rclone_config.toml',
            'rb') as fp:
            config_dict = tomllib.load(fp)

        config = Config(**config_dict)

        replicate(config)
    finally:
        rc.close()

   
# sync/sync
# srcFs (drive:src)
# dstFs (drive:dst)
# _async (true)

# job/status
# jobid (int)

if __name__ == '__main__':
    main()
