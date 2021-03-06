#!/usr/bin/python3

from retrace.retrace import (HANDLE_ARCHIVE,
                             get_active_tasks,
                             get_supported_releases,
                             response,
                             save_crashstats_reportfull)
from retrace.config import Config

CONFIG = Config()

def application(environ, start_response):
    activetasks = len(get_active_tasks())
    if activetasks >= CONFIG["MaxParallelTasks"]:
        save_crashstats_reportfull(environ["REMOTE_ADDR"])

    output = [
        "running_tasks %d" % activetasks,
        "max_running_tasks %d" % CONFIG["MaxParallelTasks"],
        "max_packed_size %d" % CONFIG["MaxPackedSize"],
        "max_unpacked_size %d" % CONFIG["MaxUnpackedSize"],
        "supported_formats %s" % " ".join(HANDLE_ARCHIVE.keys()),
        "supported_releases %s" % " ".join(get_supported_releases()),
        ]

    return response(start_response, "200 OK", "\n".join(output))
