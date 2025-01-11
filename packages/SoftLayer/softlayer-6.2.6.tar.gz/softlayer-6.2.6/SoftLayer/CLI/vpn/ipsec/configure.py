"""Request network configuration of an IPSEC tunnel context."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI.exceptions import CLIHalt


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('context_id', type=int)
@environment.pass_env
def cli(env, context_id):
    """Request configuration of a tunnel context.

    This action will update the advancedConfigurationFlag on the context
    instance and further modifications against the context will be prevented
    until all changes can be propgated to network devices.
    """
    manager = SoftLayer.IPSECManager(env.client)
    # ensure context can be retrieved by given id
    manager.get_tunnel_context(context_id)

    succeeded = manager.apply_configuration(context_id)
    if succeeded:
        click.echo(f'Configuration request received for context #{context_id}')
    else:
        raise CLIHalt(f'Failed to enqueue configuration request for context #{context_id}')
