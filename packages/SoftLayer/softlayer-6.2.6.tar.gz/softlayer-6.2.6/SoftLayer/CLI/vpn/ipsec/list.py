"""List IPSec VPN Tunnel Contexts."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.option('--sortby', help='Column to sort by',
              default='created')
@environment.pass_env
def cli(env, sortby):
    """List IPSec VPN tunnel contexts"""
    manager = SoftLayer.IPSECManager(env.client)
    contexts = manager.get_tunnel_contexts()

    table = formatting.Table(['id',
                              'name',
                              'friendly name',
                              'internal peer IP address',
                              'remote peer IP address',
                              'created'])
    table.sortby = sortby

    for context in contexts:
        table.add_row([context.get('id', ''),
                       context.get('name', ''),
                       context.get('friendlyName', ''),
                       context.get('internalPeerIpAddress', ''),
                       context.get('customerPeerIpAddress', ''),
                       context.get('createDate', '')])
    env.fout(table)
