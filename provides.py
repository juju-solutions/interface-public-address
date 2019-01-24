import json

from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class PublicAdddressProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))

    def set_address_port(self, address, port):
        # Iterate over all conversations of this type to send data to everyone.
        if type(address) is list:
            # build 2 lists to zip together that are the same length
            length = len(address)
            p = [port] * length
            combined = zip(address, p)
            clients = [{'public-address': a, 'port': p}
                       for a, p in combined]
            # for backwards compatibility, we just send a single entry
            # and have an array of dictionaries in a field of that
            # entry for the other entries.
            first = clients.pop(0)
            first['extended_data'] = json.dumps(clients)
            for relation in self.relations:
                relation.to_publish_raw.update(first)
        else:
            for relation in self.relations:
                relation.to_publish_raw.update({'public-address': address,
                                                'port': port})
