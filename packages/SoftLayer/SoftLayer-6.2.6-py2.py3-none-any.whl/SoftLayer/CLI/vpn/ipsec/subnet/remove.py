"""Remove a subnet from an IPSEC tunnel context."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI.exceptions import CLIHalt


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('context_id', type=int)
@click.option('-s',
              '--subnet-id',
              required=True,
              type=int,
              help='Subnet identifier to remove')
@click.option('-t',
              '--subnet-type',
              '--type',
              required=True,
              type=click.Choice(['internal', 'remote', 'service']),
              help='Subnet type to add')
@environment.pass_env
def cli(env, context_id, subnet_id, subnet_type):
    """Remove a subnet from an IPSEC tunnel context.

    The subnet id to remove must be specified.

    Remote subnets are deleted upon removal from a tunnel context.

    A separate configuration request should be made to realize changes on
    network devices.
    """
    manager = SoftLayer.IPSECManager(env.client)
    # ensure context can be retrieved by given id
    manager.get_tunnel_context(context_id)

    succeeded = False
    if subnet_type == 'internal':
        succeeded = manager.remove_internal_subnet(context_id, subnet_id)
    elif subnet_type == 'remote':
        succeeded = manager.remove_remote_subnet(context_id, subnet_id)
    elif subnet_type == 'service':
        succeeded = manager.remove_service_subnet(context_id, subnet_id)

    if succeeded:
        env.out(f'Removed {subnet_type} subnet #{subnet_id}')
    else:
        raise CLIHalt(f'Failed to remove {subnet_type} subnet #{subnet_id}')
