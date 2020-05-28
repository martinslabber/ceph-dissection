import logging
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

# from cephdissectionserver.db import close_pg, init_pg


async def init_app(config):

    app = web.Application()

    app["config"] = config

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader("cephdissectionserver", "templates")
    )

    # create db connection on startup, shutdown on exit
    # app.on_startup.append(init_pg)
    # app.on_cleanup.append(close_pg)
    return app


def get_config():
    config = {"host": "0.0.0.0", "port": "8000"}
    return config


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    config = get_config(argv)
    app = init_app(config)
    web.run_app(app, host=config["host"], port=config["port"])


if __name__ == "__main__":
    main(sys.argv[1:])
