import logging
import os
import socket
from io import BytesIO
from typing import TypedDict

import cbor2

from cbor2 import dumps, CBORDecoder

from rewrite_remote.handlers.project_helper import (
    find_python_files,
    parse_python_sources,
)

from rewrite_remote.remoting import (
    OK,
    RemotingMessageType,
)

from rewrite_remote.remote_utils import COMMAND_END
from rewrite_remote.remoting import RemotingContext
from rewrite_remote.handlers.handler_helpers import respond_with_error
from rewrite_remote.remoting import RemotingMessenger


class ParseProjectSourcesArgs(TypedDict):
    project_file_path: str  # The path to the individual pyproject.toml
    root_project_file_path: str  #  The path to the root pyproject.toml
    repository_dir: str  # The path to the root repository directory


def decode_parse_project_sources_args(
    decoder: CBORDecoder,
) -> ParseProjectSourcesArgs:
    """
    Decodes the arguments (order matters and must match the order encoded)
    """
    project_file_path = str(decoder.decode())
    root_project_file_path = str(decoder.decode())
    repository_dir = str(decoder.decode())

    return {
        "project_file_path": project_file_path,
        "root_project_file_path": root_project_file_path,
        "repository_dir": repository_dir,
    }


def parse_project_sources_handler(
    stream: BytesIO, sock: socket.socket, remoting_ctx: RemotingContext
) -> None:
    remoting_ctx.reset()

    # Read input from stream
    try:
        data = stream.read()
        decoder = CBORDecoder(BytesIO(data))
        args = decode_parse_project_sources_args(decoder)
        project_file_path = args.get("project_file_path")
        root_project_file_path = args.get("root_project_file_path")
        repository_dir = args.get("repository_dir")
    except Exception as e:  # pylint: disable=broad-except
        respond_with_error(f"Failed to decode arguments: {e}", sock)
        return

    if project_file_path is None:
        respond_with_error("recipe_name is required", sock)
        return

    # Log the request
    logging.info(
        "[Server] Handling parse-project-sources request: {"
        "project_file_path: %s, root_project_file_path: %s, repository_dir: %s}",
        project_file_path,
        root_project_file_path,
        repository_dir,
    )

    # Find all python files in the project
    base_dir = os.path.dirname(project_file_path)
    python_files = find_python_files(base_dir)
    source_files = parse_python_sources(python_files)

    # Write the response
    response_stream = BytesIO()
    cbor2.dump(RemotingMessageType.Response, response_stream)
    cbor2.dump(OK, response_stream)
    for source_file in source_files:
        logging.info("Sending ${source_file.source_path}")
        RemotingMessenger.send_tree(remoting_ctx, response_stream, source_file, None)
    cbor2.dump(COMMAND_END, response_stream)
    sock.sendall(response_stream.getvalue())

    logging.info("[Server] Request completed.")
