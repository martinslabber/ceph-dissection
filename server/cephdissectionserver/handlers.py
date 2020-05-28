import logging
import asyncio
import yarl
import aiohttp_jinja2
from aiohttp import web

from cephdissectionserver.processing import process_uploaded_file


async def upload_handle(request):
    # WARNING: don't do that if you plan to receive large files!
    # curl -F "datafile=@../data/osd-pool.json" http://127.0.0.1:8080/upload
    config = request.app["config"]
    req_post = await request.post()
    data_file = req_post["datafile"]
    uploaded_file = config["working_path"].joinpath(data_file.filename)
    uploaded_file.write_bytes(data_file.file.read())
    logging.info("New file %s", str(uploaded_file))
    loop = asyncio.get_event_loop()
    loop.create_task(process_uploaded_file(config, uploaded_file))

    return web.Response(text="thank you")


def server_url(request, target) -> str:
    return str(
        yarl.URL().build(host=request.host, scheme=request.scheme, path="/" + target)
    )


@aiohttp_jinja2.template("ceph-collect.sh.j2")
async def collect_handle(request):
    # TODO(MS) Low: Set return type to text.
    template_vars = {"url": server_url(request, "upload")}
    template_vars.update(request.app["config"])
    logging.debug(template_vars)
    return template_vars


@aiohttp_jinja2.template("index.j2")
async def index_handle(request):
    template_vars = {"url": server_url(request, "c")}
    template_vars.update(request.app["config"])
    logging.debug(template_vars)
    return template_vars
