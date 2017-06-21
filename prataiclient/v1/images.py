import logging

from cliff.lister import Lister
from cliff.show import ShowOne


urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.CRITICAL)
logging = logging.getLogger(__name__)


class ImageList(Lister):
    """List available runtimes"""
    def get_parser(self, prog_name):
        parser = super(ImageList, self).get_parser(prog_name)

        parser.add_argument(
            '--only-id',
            dest='only_id',
            default=False,
            action='store_true',
            help='Display only the Ids',
        )

        return parser

    def take_action(self, parsed_args):
        images = self.app.client.images.list()

        if parsed_args.only_id:
            return (('Image ID',),
                    ((image.get('image_id'),) for image in images))

        else:
            return (('Function ID', 'Name', 'Endpoint', 'Description',
                     'Memory', 'Runtime'),
                    ((image.get('function_id'),
                      image.get('name'),
                      image.get('endpoint'),
                      image.get('description'),
                      image.get('memory'),
                      image.get('runtime'),
                      ) for image in images))


class ImageShow(ShowOne):
    """Show information about a runtime"""
    def get_parser(self, prog_name):
        parser = super(ImageShow, self).get_parser(prog_name)

        parser.add_argument(dest='image_id',
                            help='id of the image')

        return parser

    def take_action(self, parsed_args):
        image = self.app.client.images.get(parsed_args.image_id)

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
            image.get('function_id', None),
            image.get('user_id', None),
            image.get('tenant_id', None),
            image.get('name', None),
            image.get('endpoint', None),
            image.get('description', None),
            image.get('type', None),
            image.get('event', None),
            image.get('runtime', None),
            image.get('memory', None),
            image.get('logs_endpoint', None)
        )
        return column, data
