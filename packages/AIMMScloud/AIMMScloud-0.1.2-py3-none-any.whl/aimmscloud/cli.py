# coding: utf-8

"""
    AIMMS Cloud rest API client Command Line Interface
"""

import sys

try:
    import click
except ImportError:
    sys.stderr.write(
        "It seems aimmscloud is not installed with cli option. \n"
        'Run pip install "aimmscloud[cli]" to fix this.'
    )
    sys.exit(1)


def _get_application_api(ctx: click.Context):
    url = ctx.obj["url"]
    key = ctx.obj["key"]
    from aimmscloud.aimms_application import Application

    app = Application(url, key)
    return app


@click.group()
@click.option(
    "-u",
    "--url",
    default=False,
    type=click.STRING,
    help="The host url of the AIMMS account you work with. For example: `https://myaccount.aimms.cloud/pro-api/v2`",
)
@click.option(
    "-k",
    "--key",
    default="always",
    type=click.STRING,
    help="The api_key you created to authenicat with the AIMMS Cloud API. or more information please look at: https://documentation.aimms.com/cloud/rest-api.html#api-keys-and-scopes",
)
@click.pass_context
def cli(ctx: click.Context, url: str, key: str) -> None:
    # Set the context object to pass the url and key to the subcommands
    ctx.obj = {"url": url, "key": key}


@cli.command()
@click.pass_context
def get_aimms_versions(ctx: click.Context) -> None:
    """Display the available AIMMS versions."""
    app = _get_application_api(ctx)
    versions = app.get_aimms_versions()
    click.echo(versions)


@cli.command()
@click.pass_context
@click.option(
    "--category-name",
    default="test",
    type=click.STRING,
    help="The name of the new category to create.",
)
def create_app_category(ctx: click.Context, category_name: str) -> None:
    """Create a new application category."""
    app = _get_application_api(ctx)
    app.create_app_category()
    click.echo("create_app_category")


@cli.command()
@click.pass_context
@click.option(
    "--project-name",
    default="test",
    type=click.STRING,
    help="The name of the application to delete.",
)
@click.option(
    "--project-version",
    default="test",
    type=click.STRING,
    help="The version of the application to delete.",
)
def delete_app(ctx: click.Context, project_name: str, project_version: str) -> None:
    """Delete an application."""
    app = _get_application_api(ctx)
    app.delete_app(project_name, project_version)
    click.echo("deleted app")


@cli.command()
@click.pass_context
def get_all_app_categories(ctx: click.Context) -> None:
    """Get all application categories."""
    app = _get_application_api(ctx)
    out = app.get_all_app_categories()
    click.echo(out)


@cli.command()
@click.pass_context
def get_all_apps_info(ctx: click.Context) -> None:
    """Get all applications and their meta data."""
    app = _get_application_api(ctx)
    out = app.get_all_apps_info()
    click.echo(out)


@cli.command()
@click.pass_context
@click.option(
    "--file-name",
    type=click.STRING,
    help="The name of the file to publish.",
    required=True,
)
@click.option(
    "--iconfile-name",
    type=click.STRING,
    help="The name of the icon file to publish.",
    required=True,
)
@click.option(
    "--aimms-version",
    type=click.STRING,
    help="The version of AIMMS to use.",
    required=True,
)
@click.option(
    "--application-description",
    type=click.STRING,
    help="The description of the application.",
    required=True,
)
@click.option(
    "--application-name",
    type=click.STRING,
    help="The name of the application.",
    required=True,
)
@click.option(
    "--application-version",
    type=click.STRING,
    help="The version of the application.",
    required=True,
)
@click.option(
    "--attributes",
    type=click.STRING,
    help="dictionary with the specific metadata for publishing such as isWebUI, ServerLicense, etc.",
    required=False,
)
@click.option(
    "--projectCategory",
    type=click.STRING,
    help="The category of the application.",
    required=False,
)
@click.option(
    "--publish-behavior",
    type=click.INT,
    help="0 to publish new application, 1 to update existing application",
    required=False,
)
def publish_app(
    ctx: click.Context,
    file_name: str,
    iconfile_name: str,
    aimms_version: str,
    application_description: str,
    application_name: str,
    application_version: str,
    attributes: dict,
    projectCategory: str = "",
    publish_behavior: int = 1,
    metadata: dict = None,
) -> None:
    """Publish an application."""
    app = _get_application_api(ctx)
    out = app.publish_app(
        file_name,
        iconfile_name,
        aimms_version,
        application_description,
        application_name,
        application_version,
        attributes,
        projectCategory,
        publish_behavior,
        metadata,
    )
    click.echo(out)


if __name__ == "__main__":
    cli()
