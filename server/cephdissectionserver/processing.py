import logging
import asyncio


def fsid_time_fromfilename(filename):
    fparts = filename.stem.split("-")
    fsid = "-".join(fparts[1:6])
    timestamp = fparts[6]
    return fsid, timestamp


async def process_uploaded_file(config, filename):

    await asyncio.sleep(1)
    logging.info("Processing %s", filename)
    fsid, timestamp = fsid_time_fromfilename(filename)
    logging.info("Data for fsid=%s @ %s", fsid, timestamp)
    fsid_path = config["storage_path"].joinpath(fsid)
    fsid_path.mkdir(exist_ok=True)
    ts_path = fsid_path.joinpath(timestamp)
    ts_path.mkdir(exist_ok=True)
    new_filename = ts_path.joinpath(filename.name)
    filename.rename(new_filename)
    logging.info("Moved file to %s", new_filename)
    await asyncio.sleep(0)
