#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
import os
import sys
from argparse import ArgumentParser

from brainframe.api import BrainFrameAPI, bf_errors
from brainframe_apps.command_utils import by_name, command, subcommand_parse_args
from brainframe_apps.logger_factory import log


def get_stream_persistent_id(stream):
    if "url" in stream.connection_options:
        return stream.connection_options["url"]
    elif "storage_id" in stream.connection_options:
        return stream.connection_options["storage_id"]
    else:
        raise ValueError("no stream persistent id available")


class NextBFStream:
    def __init__(self, api, last_stream_persistent_id):
        self.streams = None

        if api is None:
            log.error("The BrainFrame api is None")
            return

        streams = api.get_stream_configurations()
        if not streams:
            return

        self.streams = sorted(streams, key=lambda x: x.id)

        self.last_stream_persistent_id = last_stream_persistent_id

        return

    def __iter__(self):
        return self

    def __next__(self):
        if self.streams is None:
            raise StopIteration

        for i, stream in enumerate(self.streams):
            stream_persistent_id = get_stream_persistent_id(stream)
            if not self.last_stream_persistent_id:
                # This should be the first stream
                self.last_stream_persistent_id = stream_persistent_id
                return stream

            else:
                if stream_persistent_id == self.last_stream_persistent_id:
                    # Found the last stream
                    if i + 1 < len(self.streams):
                        stream = self.streams[i + 1]
                        # before returning the stream, we need to track the last stream
                        self.last_stream_persistent_id = get_stream_persistent_id(
                            stream
                        )
                        return stream
                    else:
                        # End of the list, break and stop the iteration
                        break

        raise StopIteration


def stream_status(api, stream, id):
    if stream is None:
        return None, None, None

    analyze = api.check_analyzing(id)
    stream_persistent_id = get_stream_persistent_id(stream)

    if analyze:
        analyze_status = "A"
        if stream.runtime_options:
            keyframes_only = stream.runtime_options["keyframes_only"]
            if keyframes_only:
                keyframes_only_status = "K"
            else:
                keyframes_only_status = "-"
        else:
            keyframes_only_status = "-"
    else:
        analyze_status = "-"
        keyframes_only_status = "-"

    return analyze_status, keyframes_only_status, stream_persistent_id


def get_stream_id(api, match_stream_persistent_id):
    streams = api.get_stream_configurations()

    for stream in streams:
        stream_persistent_id = get_stream_persistent_id(stream)
        if stream_persistent_id == match_stream_persistent_id:
            return stream.id
    return None


def list_stream_capsules(api, stream_id):
    if api:
        log.debug(f"capsules on BrainFrame server: {api._server_url} {api.version()}:")
        for capsule in api.get_capsules():
            if api.is_capsule_active(capsule.name):
                capsule_status_flag = "Active"
            else:
                capsule_status_flag = "      "
            global_options = api.get_capsule_option_vals(capsule.name, stream_id)
            log.debug(f"    * {capsule_status_flag} {capsule.name} {global_options}")


def list_stream(api, stream_persistent_id=None, show_capsules=False):
    streams = NextBFStream(api, stream_persistent_id)
    if not streams:
        log.warning(f"No stream found!")
    else:
        log.debug("Analyze Status: A/-, Keyframes Only: K/-")
        log.debug(
            f'{"Idx":3}. {"sID":>5} {"A/-":>2} {"K/-":>2} {"Stream Name":>39} {"Stream URL":>40}'
        )

    stream = None
    if stream_persistent_id is None and streams is not None:
        for i, stream in enumerate(streams):

            if stream is None:
                continue
            analyze_status, keyframes_only_status, stream_url = stream_status(
                api, stream, stream.id
            )
            log.debug(
                f"{i + 1:3}. {stream.id} {analyze_status:>2}  {keyframes_only_status:>2} {stream.name:>40} {stream_url:>40}",
            )
            if show_capsules:
                list_stream_capsules(api, stream.id)
        else:
            pass
    else:
        try:
            if streams is None:
                return None
            stream = next(streams)
            log.debug(
                f'    {stream.id} {stream.name} {stream.connection_options["url"]}',
            )
        except:
            log.debug(f"    None")

    return stream


def list_stream_parse_args(parser):
    parser.add_argument(
        "--server-url",
        default="http://localhost",
        help="The URL for the BrainFrame server.",
    )
    parser.add_argument(
        "--stream-url",
        default=None,
        help="A stream persistent id, either the stream urls or storage id. Default: %(default)s",
    )


@command("list_stream")
def list_stream_main():
    parser = ArgumentParser(
        description="This tool lists video streams of the BrainFrame server."
    )
    list_stream_parse_args(parser)
    args = subcommand_parse_args(parser)

    # Connect to the BrainFrame Server
    server_url = args.server_url if args.server_url else f"http://{args.server_url}"
    print(
        f"\n{os.path.basename(sys.argv[0])} Waiting for BrainFrame server at {server_url}"
    )
    api = BrainFrameAPI(server_url)
    try:
        api.wait_for_server_initialization(timeout=15)
    except (TimeoutError, bf_errors.ServerNotReadyError):
        print(f"BrainFrame server connection timeout")
        return

    stream = list_stream(api, args.stream_url)
    if stream is None:
        print("\nNo stream found")


if __name__ == "__main__":
    by_name["list_stream"]()
