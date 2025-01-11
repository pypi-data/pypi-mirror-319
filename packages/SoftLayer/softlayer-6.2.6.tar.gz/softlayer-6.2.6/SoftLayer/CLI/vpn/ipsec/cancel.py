"""Cancel an IPSec service."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import formatting


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('identifier')
@click.option('--immediate',
              is_flag=True,
              default=False,
              help="Cancels the service  immediately (instead of on the billing anniversary)")
@click.option('--reason',
              help="An optional cancellation reason. See cancel-reasons for a list of available options")
@click.option('--force', default=False, is_flag=True, help="Force cancel ipsec vpn without confirmation")
@environment.pass_env
def cli(env, identifier, immediate, reason, force):
    """Cancel a IPSEC VPN tunnel context."""

    manager = SoftLayer.IPSECManager(env.client)
    context = manager.get_tunnel_context(identifier, mask='billingItem')

    if 'billingItem' not in context:
        raise SoftLayer.SoftLayerError("Cannot locate billing. May already be cancelled.")

    if not force:
        if not (env.skip_confirmations or
                formatting.confirm("This will cancel the Ipsec Vpn and cannot be undone. Continue?")):
            raise exceptions.CLIAbort('Aborted')

    result = manager.cancel_item(context['billingItem']['id'], immediate, reason)

    if result:
        env.fout(f"Ipsec {identifier} was cancelled.")
