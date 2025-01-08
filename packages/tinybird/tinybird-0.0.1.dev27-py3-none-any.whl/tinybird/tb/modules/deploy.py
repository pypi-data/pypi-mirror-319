import glob
import json
import logging
import time
from pathlib import Path
from typing import List

import click
import requests

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.feedback_manager import FeedbackManager


def project_files(project_path: Path) -> List[str]:
    project_file_extensions = ("datasource", "pipe")
    project_files = []
    for extension in project_file_extensions:
        for project_file in glob.glob(f"{project_path}/**/*.{extension}", recursive=True):
            logging.debug(f"Found project file: {project_file}")
            project_files.append(project_file)
    return project_files


def promote_deployment(host: str, headers: dict) -> None:
    TINYBIRD_API_URL = host + "/v1/deployments"
    r = requests.get(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))

    deployments = result.get("deployments")
    if not deployments:
        click.echo(FeedbackManager.error(message="No deployments found"))
        return

    last_deployment, candidate_deployment = deployments[0], deployments[1]

    if candidate_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Current deployment is not ready"))
        return

    if candidate_deployment.get("live"):
        click.echo(FeedbackManager.error(message="Candidate deployment is already live"))
    else:
        click.echo(FeedbackManager.success(message="Promoting deployment"))

        TINYBIRD_API_URL = host + f"/v1/deployments/{candidate_deployment.get('id')}/set-live"
        r = requests.post(TINYBIRD_API_URL, headers=headers)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))

    click.echo(FeedbackManager.success(message="Removing old deployment"))

    TINYBIRD_API_URL = host + f"/v1/deployments/{last_deployment.get('id')}"
    r = requests.delete(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))

    click.echo(FeedbackManager.success(message="Deployment promoted successfully"))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True), default=Path.cwd())
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=False,
    help="Auto-promote the deployment. Only works if --wait is enabled. Disabled by default.",
)
def deploy(project_path: Path, wait: bool, auto: bool) -> None:
    """
    Validate and deploy the project server side.
    """
    # TODO: This code is duplicated in build_server.py
    # Should be refactored to be shared
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
    }

    config = CLIConfig.get_project_config(str(project_path))
    TINYBIRD_API_URL = (config.get_host() or "") + "/v1/deploy"
    TINYBIRD_API_KEY = config.get_token()

    files = [
        ("context://", ("cli-version", "1.0.0", "text/plain")),
    ]
    fds = []
    for file_path in project_files(project_path):
        relative_path = str(Path(file_path).relative_to(project_path))
        fd = open(file_path, "rb")
        fds.append(fd)
        content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
        files.append((MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd.read().decode("utf-8"), content_type)))

    deployment = None
    try:
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))

        deploy_result = result.get("result")
        if deploy_result == "success":
            click.echo(FeedbackManager.success(message="Deploy submitted successfully"))
            deployment = result.get("deployment")
        elif deploy_result == "failed":
            click.echo(FeedbackManager.error(message="Deploy failed"))
            deploy_errors = result.get("errors")
            for deploy_error in deploy_errors:
                if deploy_error.get("filename", None):
                    click.echo(
                        FeedbackManager.error(message=f"{deploy_error.get('filename')}\n\n{deploy_error.get('error')}")
                    )
                else:
                    click.echo(FeedbackManager.error(message=f"{deploy_error.get('error')}"))
        else:
            click.echo(FeedbackManager.error(message=f"Unknown build result {deploy_result}"))
    finally:
        for fd in fds:
            fd.close()

    if deployment and wait:
        while deployment.get("status") != "data_ready":
            time.sleep(5)
            TINYBIRD_API_URL = (config.get_host() or "") + f"/v1/deployments/{deployment.get('id')}"
            r = requests.get(TINYBIRD_API_URL, headers=HEADERS)
            result = r.json()
            deployment = result.get("deployment")
            if deployment.get("status") == "failed":
                click.echo(FeedbackManager.error(message="Deployment failed"))
                return

        click.echo(FeedbackManager.success(message="Deployment is ready"))

        if auto:
            promote_deployment((config.get_host() or ""), HEADERS)


@cli.command(name="release")
@click.argument("project_path", type=click.Path(exists=True), default=Path.cwd())
def deploy_promote(project_path: Path) -> None:
    """
    Promote last deploy to ready and remove old one.
    """
    config = CLIConfig.get_project_config(str(project_path))

    TINYBIRD_API_KEY = config.get_token()
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    promote_deployment((config.get_host() or ""), HEADERS)
