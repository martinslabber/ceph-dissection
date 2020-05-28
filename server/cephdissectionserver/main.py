import logging

from pathlib import Path
import aiohttp_jinja2
import jinja2
from aiohttp import web
import configargparse

import cephdissectionserver.handlers as handlers

# from cephdissectionserver.db import close_pg, init_pg


async def init_app(config):

    app = web.Application(client_max_size=(1 + config["max_upload_size"]) * 1024 ** 2)

    app["config"] = config

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader("cephdissectionserver", "templates")
    )

    # create db connection on startup, shutdown on exit
    # app.on_startup.append(init_pg)
    # app.on_cleanup.append(close_pg)
    app.add_routes(
        [
            web.get("/", handlers.index_handle),
            web.post("/upload", handlers.upload_handle),
            web.get("/collect", handlers.collect_handle),
            web.get("/c", handlers.collect_handle),  # Supper lazy shorthand
            # web.get("/metrics", collect_handle),
        ]
    )
    return app


def pick_logging_level(config: dict) -> int:

    level = logging.WARNING
    if config["debug"]:
        return logging.DEBUG
    if config["verbose"]:
        level -= 10
    if config["quiet"]:
        level += 10

    return level


def get_config() -> dict:

    p = configargparse.ArgParser(default_config_files=["./cephviz.conf"])
    p.add("-c", "--config", required=True, is_config_file=True, help="config file path")
    p.add("-v", help="verbose", action="store_true")
    p.add("-q", help="quiet", action="store_true")
    p.add("--debug", help="debug", action="store_true")
    p.add("--dsn", help="Database connection string DSN")
    p.add("-s", "--storage-path", help="Path where collection files will be stored")
    p.add(
        "-w",
        "--working-path",
        help="Path where collection files will be unpacked (temp)",
    )
    p.add("-p", "--port", help="bind port")
    p.add("-a", "--address", help="bind address")
    p.add(
        "--max-upload-size",
        type=int,
        help="The maximum size in MiB that can be uploaded.",
    )
    options = vars(p.parse_args())
    options["verbose"] = options.pop("v", False)
    options["quiet"] = options.pop("q", False)
    options["config_filename"] = options.pop("config", None)
    options["storage_path"] = Path(options["storage_path"])
    options["working_path"] = Path(options["working_path"])

    # Set up logging
    logging.basicConfig(level=pick_logging_level(options))
    logging.debug("Running config is %s", p.format_values())
    return options


def main():
    config = get_config()
    app = init_app(config)
    web.run_app(app, port=config["port"])


if __name__ == "__main__":
    main()
