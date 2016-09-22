from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class PublicAddressProvides(RelationBase):
    '''This class provides a public address and port to other units.'''
    scope = scopes.UNIT

    @hook('{provides:public-address}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:public-address}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    def set_address_port(self, address, port):
        # Iterate over all conversations of this type to send data to everyone.
        for conversation in self.conversations():
            client = {'address': address, 'port': port}
            # Send the address and port to every unit using the conversation.
            conversation.set_remote(data=client)
