import json

from charms.reactive import when, set_flag, Endpoint
from charms.reactive.flags import register_trigger


class PublicAddressRequires(Endpoint):
    def register_triggers(self):
        register_trigger(
            when_not=self.expand_name('endpoint.{endpoint_name}.joined'),
            clear_flag=self.expand_name('{endpoint_name}.available')
        )

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received_raw['port'] and
               unit.received_raw['public-address']
               for unit in self.all_joined_units):
            set_flag(self.expand_name('{endpoint_name}.available'))

    def get_addresses_ports(self):
        '''Returns a list of available HTTP providers and their associated
        public addresses and ports.

        The return value is a list of dicts of the following form::
            [
                {
                    'public-address': address_of_host,
                    'port': port_for_host,
                },
                # ...
            ]
        '''
        hosts = set()
        for relation in self.relations:
            for unit in relation.joined_units:
                data = unit.received_raw
                hosts.add((data['public-address'], data['port']))
                if 'extended_data' in data:
                    for ed in json.loads(data['extended_data']):
                        hosts.add((ed['public-address'], ed['port']))

        return [{'public-address': pa, 'port': p} for pa, p in sorted(hosts)]
