#!/usr/bin/python

# Copyright (C) 2020 Daniel Mueller <deso@posteo.net>
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import (
  ArgumentParser,
)
from contextlib import (
  suppress,
)
from mimetypes import (
  add_type,
)
from os import (
  chdir,
)
from http.server import (
  HTTPServer,
  SimpleHTTPRequestHandler,
)

from sys import (
  argv,
  exit,
)

DEFAULT_ADDRESS = ""
DEFAULT_PORT = 8080


def serve(address=DEFAULT_ADDRESS, port=DEFAULT_PORT, ext_map=None):
  """Serve HTTP. Forever."""
  for (k, v) in ext_map.items():
    add_type(k, v)
    SimpleHTTPRequestHandler.extensions_map[k] = v

  httpd = HTTPServer((address, port), SimpleHTTPRequestHandler)

  with suppress(KeyboardInterrupt):
    httpd.serve_forever()


def main(args):
  """Start a web server."""
  parser = ArgumentParser()
  parser.add_argument(
    "-a", "--address", action="store", default="",
    help="Change the address to listen on (defaults to \"{DEFAULT_ADDRESS\").",
  )
  parser.add_argument(
    "-d", "--directory", action="store",
    help=("Change into the given directory before serving instead of "
          "staying in the current working directory."),
  )
  parser.add_argument(
    "-p", "--port", action="store", type=int, default=DEFAULT_PORT,
    help="The port to listen on (defaults to {DEFAULT_PORT}).",
  )
  parsed = parser.parse_args(args)

  if parsed.directory is not None:
    chdir(parsed.directory)

  # TODO: Should be made configurable through arguments as well.
  ext_map = {
    ".js": "text/javascript",
    ".wasm": "application/wasm",
  }

  print(f"Serving at http://{parsed.address}:{parsed.port}/")
  with suppress(KeyboardInterrupt):
    serve(parsed.address, parsed.port, ext_map)
  return 0


if __name__ == "__main__":
  exit(main(argv[1:]))
