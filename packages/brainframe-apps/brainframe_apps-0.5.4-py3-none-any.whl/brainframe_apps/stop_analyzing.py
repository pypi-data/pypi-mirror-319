#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
import os
from argparse import ArgumentParser

from brainframe.api import BrainFrameAPI, bf_errors
from brainframe_apps.command_utils import by_name, command, subcommand_parse_args
from brainframe_apps.logger_factory import log
from brainframe_apps.start_analyzing import (
    analyzing_on_off_all,
    analyzing_on_off_persistent_id,
    start_analyzing_parse_args,
)
from brainframe_apps.urls import UrlList, get_ip


def stop_analyzing(api, stream_url):
    stream_id = analyzing_on_off_persistent_id(api, stream_url, False, False)

    if stream_id is not None:
        log.debug(f"{os.path.basename(__file__)}: {stream_url} succeeded: {stream_id}")
    else:
        log.error(f"{os.path.basename(__file__)}: {stream_url} failed")

    return stream_id


def stop_analyzing_all(api):
    analyzing_on_off_all(api, False)


@command("stop_analyzing")
def stop_analyzing_main():
    parser = ArgumentParser(description="Stop analyze a BrainFrame video stream")
    start_analyzing_parse_args(parser)
    args = subcommand_parse_args(parser)

    # Connect to BrainFrame server
    api = BrainFrameAPI(args.server_url)

    log.debug(f"{str(parser.prog)} Waiting for server at {args.server_url} ...")

    try:
        api.wait_for_server_initialization(timeout=15)
    except (TimeoutError, bf_errors.ServerNotReadyError):
        log.error(f"BrainFrame server connection timeout")
        return

    if args.stream_url is not None:
        stream_url = args.stream_url.replace("localhost", str(get_ip()))

        stream_id = stop_analyzing(api, stream_url)

        if stream_id is not None:
            log.debug(f"{stream_id} {stream_url}: analyzing has stopped")
        else:
            log.error(f"{stream_id} {stream_url}: stop analyzing has failed")
    else:
        stream_id = stop_analyzing_all(api)
    return stream_id


if __name__ == "__main__":
    by_name["stop_analyzing"]()
