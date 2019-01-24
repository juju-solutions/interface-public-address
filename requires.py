import json

from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class PublicAddressRequires(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received_raw['port'] and
               unit.received_raw['public-address']
               for unit in self.all_joined_units):
            set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

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
        hosts = []
        dup_list = {}
        for relation in self.relations:
            for unit in relation.joined_units:
                data = unit.received_raw
                # remove duplicates
                key = '{}.{}'.format(data['public-address'],
                                     data['port'])
                if key not in dup_list:
                    dup_list[key] = 1
                    hosts.append({'public-address': data['public-address'],
                                  'port': data['port']})
                if 'extended_data' in data:
                    for ed in json.loads(data['extended_data']):
                        # remove duplicates
                        key = '{}.{}'.format(data['public-address'],
                                             data['port'])
                        if key not in dup_list:
                            dup_list[key] = 1
                            host = {'public-address': ed['public-address'],
                                    'port': ed['port']}
                            hosts.append(host)

        return hosts
