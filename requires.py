from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class PublicAddressRequires(RelationBase):
    '''The class that requires a public address to another unit.'''
    scope = scopes.UNIT

    @hook('{requires:public-address}-relation-{joined,changed}')
    def changed(self):
        conversation = self.conversation()
        if conversation.get_remote('port'):
            # this unit's conversation has a port, so
            # it is part of the set of available units
            conversation.set_state('{relation_name}.available')

    @hook('{requires:public-address}-relation-{departed,broken}')
    def broken(self):
        conversation = self.conversation()
        conversation.remove_state('{relation_name}.available')

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
        for conversation in self.conversations():
            address = conversation.get_remote('public-address')
            port = conversation.get_remote('port')
            if address and port:
                hosts.append({'public-address': address, 'port': port})
        return hosts
