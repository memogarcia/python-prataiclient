import logging

from cliff.lister import Lister
from cliff.show import ShowOne


urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.CRITICAL)
logging = logging.getLogger(__name__)

# TODO(m3m0): use the correct structure


class EventList(Lister):
    """List available events to hook up"""
    def get_parser(self, prog_name):
        parser = super(EventList, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        events = self.app.client.events.list()

        return (('Function ID', 'Name', 'Endpoint', 'Description',
                 'Memory', 'Runtime'),
                ((event.get('function_id'),
                  event.get('name'),
                  event.get('endpoint'),
                  event.get('description'),
                  event.get('memory'),
                  event.get('runtime'),
                  ) for event in events))


class EventShow(ShowOne):
    """Show information about an event"""
    def get_parser(self, prog_name):
        parser = super(EventShow, self).get_parser(prog_name)

        parser.add_argument(dest='event_id',
                            help='id of the event')

        return parser

    def take_action(self, parsed_args):
        event = self.app.client.events.get(parsed_args.event_id)

        column = (
            'function_id',
            'user_id',
            'tenant_id',
            'name',
            'endpoint',
            'description',
            'type',
            'event',
            'runtime',
            'memory',
            'logs_endpoint'
        )
        data = (
            event.get('function_id', None),
            event.get('user_id', None),
            event.get('tenant_id', None),
            event.get('name', None),
            event.get('endpoint', None),
            event.get('description', None),
            event.get('type', None),
            event.get('event', None),
            event.get('runtime', None),
            event.get('memory', None),
            event.get('logs_endpoint', None)
        )
        return column, data
