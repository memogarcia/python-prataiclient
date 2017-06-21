import logging

from cliff.lister import Lister


urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.CRITICAL)
logging = logging.getLogger(__name__)


class ClusterStatus(Lister):
    """Show information about the cluster"""
    def get_parser(self, prog_name):
        parser = super(ClusterStatus, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        # TODO(m3m0): check cluster data structure
        components = self.app.client.cluster.status()

        return (('Component ID', 'Type', 'Joined At', 'Status'),
                ((component.get('daemon_id'),
                  component.get('daemon_type'),
                  component.get('joined_at'),
                  component.get('status'),
                  ) for component in components))
