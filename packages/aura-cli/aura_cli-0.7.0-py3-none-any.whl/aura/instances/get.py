import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(name="get", help_text="Get details for an instance")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option("--name", "-n", help="The instance name")
def get_instance(instance_id: str, name: str):
    """
    Get details of an instance.

    Makes "GET /instances/:instanceId" API request.
    """

    instance_id = get_instance_id(instance_id, name)

    path = f"/instances/{instance_id}"

    return make_api_call("GET", path)
