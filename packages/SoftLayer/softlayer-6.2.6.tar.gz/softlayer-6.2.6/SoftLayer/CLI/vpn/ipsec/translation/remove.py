"""Remove a translation entry from an IPSEC tunnel context."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI.exceptions import CLIHalt


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('context_id', type=int)
@click.option('-t',
              '--translation-id',
              required=True,
              type=int,
              help='Translation identifier to remove')
@environment.pass_env
def cli(env, context_id, translation_id):
    """Remove a translation entry from an IPSEC tunnel context.

    A separate configuration request should be made to realize changes on
    network devices.
    """
    manager = SoftLayer.IPSECManager(env.client)
    # ensure translation can be retrieved by given id
    manager.get_translation(context_id, translation_id)

    succeeded = manager.remove_translation(context_id, translation_id)
    if succeeded:
        env.out(f'Removed translation #{translation_id}')
    else:
        raise CLIHalt(f'Failed to remove translation #{translation_id}')
