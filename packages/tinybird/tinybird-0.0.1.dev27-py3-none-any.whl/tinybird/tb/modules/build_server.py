import asyncio
import glob
import json
import logging
from pathlib import Path
from typing import List

import click
import requests

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client


def project_files(project_path: Path) -> List[str]:
    project_file_extensions = ("datasource", "pipe")
    project_files = []
    for extension in project_file_extensions:
        for project_file in glob.glob(f"{project_path}/**/*.{extension}", recursive=True):
            logging.debug(f"Found project file: {project_file}")
            project_files.append(project_file)
    return project_files


@cli.command()
@click.argument("project_path", type=click.Path(exists=True), default=Path.cwd())
def build_server(project_path: Path) -> None:
    """
    Validate and build the project server side.
    """

    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
    }

    tb_client = asyncio.run(get_tinybird_local_client(str(project_path)))
    TINYBIRD_API_URL = tb_client.host + "/v1/build"
    TINYBIRD_API_KEY = tb_client.token

    files = [
        ("context://", ("cli-version", "1.0.0", "text/plain")),
    ]
    fds = []
    for file_path in project_files(project_path):
        relative_path = str(Path(file_path).relative_to(project_path))
        fd = open(file_path, "rb")
        fds.append(fd)
        content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
        files.append((MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd, content_type)))

    try:
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))

        build_result = result.get("result")
        if build_result == "success":
            click.echo(FeedbackManager.success(message="Build completed successfully"))
        elif build_result == "failed":
            click.echo(FeedbackManager.error(message="Build failed"))
            build_errors = result.get("errors")
            for build_error in build_errors:
                click.echo(
                    FeedbackManager.error(message=f"{build_error.get('filename')}\n\n{build_error.get('error')}")
                )
        else:
            click.echo(FeedbackManager.error(message=f"Unknown build result. Error: {result.get('error')}"))
    finally:
        for fd in fds:
            fd.close()
