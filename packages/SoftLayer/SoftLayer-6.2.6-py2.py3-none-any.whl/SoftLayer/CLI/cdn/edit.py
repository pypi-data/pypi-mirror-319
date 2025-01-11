"""Edit a CDN Account."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.argument('identifier')
@click.option('--header', '-H',
              type=click.STRING,
              help="Host header."
              )
@click.option('--http-port', '-t',
              type=click.INT,
              help="HTTP port."
              )
@click.option('--https-port', '-s',
              type=click.INT,
              help="HTTPS port."
              )
@click.option('--origin', '-o',
              type=click.STRING,
              help="Origin server address."
              )
@click.option('--respect-headers', '-r',
              type=click.Choice(['1', '0']),
              help="Respect headers. The value 1 is On and 0 is Off."
              )
@click.option('--cache', '-c', type=str,
              help="Cache key optimization. These are the valid options to choose: 'include-all', 'ignore-all', "
                   "'include-specified', 'ignore-specified'. If you select 'include-specified' or 'ignore-specified' "
                   "please add to option --cache-description.\n"
                   " e.g --cache=include-specified --cache-description=description."
              )
@click.option('--cache-description', '-C', type=str,
              help="In cache option, if you select 'include-specified' or 'ignore-specified', "
                   "please add a description too using this option.\n"
                   "e.g --cache include-specified --cache-description description."
              )
@click.option('--performance-configuration', '-p',
              type=click.Choice(['General web delivery', 'Large file optimization', 'Video on demand optimization']),
              help="Optimize for, General web delivery', 'Large file optimization', 'Video on demand optimization', "
                   "the Dynamic content acceleration option is not added because this has a special configuration."
              )
@environment.pass_env
def cli(env, identifier, header, http_port, https_port, origin, respect_headers, cache,
        cache_description, performance_configuration):
    """Edit a CDN Account.

       Note: You can use the hostname or uniqueId as IDENTIFIER.
    """

    manager = SoftLayer.CDNManager(env.client)
    cdn_id = helpers.resolve_id(manager.resolve_ids, identifier, 'CDN')

    cache_result = {}
    if cache or cache_description:
        if len(cache) > 1:
            cache_result['cacheKeyQueryRule'] = cache
        else:
            cache_result['cacheKeyQueryRule'] = cache[0]

    cdn_result = manager.edit(cdn_id, header=header, http_port=http_port, https_port=https_port, origin=origin,
                              respect_headers=respect_headers, cache=cache_result, cache_description=cache_description,
                              performance_configuration=performance_configuration)

    table = formatting.KeyValueTable(['name', 'value'])
    table.align['name'] = 'r'
    table.align['value'] = 'l'

    for cdn in cdn_result:
        table.add_row(['Create Date', cdn.get('createDate')])
        table.add_row(['Header', cdn.get('header')])
        if cdn.get('httpPort'):
            table.add_row(['Http Port', cdn.get('httpPort')])
        if cdn.get('httpsPort'):
            table.add_row(['Https Port', cdn.get('httpsPort')])
        table.add_row(['Origin Type', cdn.get('originType')])
        table.add_row(['Performance Configuration', cdn.get('performanceConfiguration')])
        table.add_row(['Protocol', cdn.get('protocol')])
        table.add_row(['Respect Headers', cdn.get('respectHeaders')])
        table.add_row(['Unique Id', cdn.get('uniqueId')])
        table.add_row(['Vendor Name', cdn.get('vendorName')])
        table.add_row(['Cache key optimization', cdn.get('cacheKeyQueryRule')])
        table.add_row(['cname', cdn.get('cname')])
        table.add_row(['Origin server address', cdn.get('originHost')])

    env.fout(table)
