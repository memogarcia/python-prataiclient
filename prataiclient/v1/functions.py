import logging
import json
from io import StringIO

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from prataiclient import utils


urllib3_logger = logging.getLogger('requests')
urllib3_logger.setLevel(logging.CRITICAL)
logging = logging.getLogger(__name__)


class FunctionShow(ShowOne):
    """Show information about a function"""
    def get_parser(self, prog_name):
        parser = super(FunctionShow, self).get_parser(prog_name)
        
        parser.add_argument(dest='function_id',
                            help='id of the function')
                            
        return parser
        
    def take_action(self, parsed_args):
        function = self.app.client.functions.get(parsed_args.function_id)

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
        log_endpoint = '{0}/logs'.format(function.get('endpoint', ''))
        data = (
            function.get('function_id', None),
            function.get('user_id', None),
            function.get('tenant_id', None),
            function.get('name', None),
            function.get('endpoint', None),
            function.get('description', None),
            function.get('type', None),
            function.get('event', None),
            function.get('runtime', None),
            function.get('memory', None),
            log_endpoint
        )
        return column, data


class FunctionCreate(Command):
    """Create a function from a file"""
    def get_parser(self, prog_name):
        parser = super(FunctionCreate, self).get_parser(prog_name)
        
        parser.add_argument(dest='name',
                            help='name of the function')
                            
        parser.add_argument('--description',
                            dest='description',
                            default='',
                            help='Description of the function')
        
        parser.add_argument('--zip',
                            dest='zip',
                            required=True,
                            help='Path to zip file with the function '
                                 'and requirements are stored.')
                            
        parser.add_argument('--memory',
                            dest='memory',
                            default=128,
                            help='How much memory this function will '
                                 'have available, default 128, '
                                 'min value = 64, max value = 8192')
        
        parser.add_argument('--type',
                            dest='type',
                            default='async',
                            choices=['async', 'wait_for_response'],
                            help='async will execute the function in the '
                                 'background, wait_for_response will block '
                                 'the execution until a response is given.')
                            
        parser.add_argument('--runtime',
                            dest='runtime',
                            default='python27',
                            help='Define language runtime')
                            
        parser.add_argument('--event',
                            dest='event',
                            default='webhook',
                            help='Define an event for the function to '
                                 'subscribe to')

        return parser

    def take_action(self, parsed_args):
        metadata = {}
        metadata['name'] = parsed_args.name
        metadata['description'] = parsed_args.description or ''
        metadata['event'] = parsed_args.event or 'webhook'
        metadata['runtime'] = parsed_args.runtime or 'python27'
        metadata['type'] = parsed_args.type or 'async'
        metadata['memory'] = parsed_args.memory or 128

        meta = json.dumps(metadata)
        fd_meta = StringIO(meta)

        files = {
            "zip_file": open(parsed_args.zip),
            "metadata": fd_meta
        }

        response = self.app.client.functions.create(files)
        logging.info(response)


class FunctionList(Lister):
    """List all functions"""
    def get_parser(self, prog_name):
        parser = super(FunctionList, self).get_parser(prog_name)

        parser.add_argument(
            '--only-id',
            dest='only_id',
            default=False,
            action='store_true',
            help='Display only the Ids',
        )

        return parser

    def take_action(self, parsed_args):
        functions = self.app.client.functions.list()

        if parsed_args.only_id:
            return (('Function ID',),
                    ((function.get('function_id'),) for function in functions))

        else:
            return (('Function ID', 'Name', 'Endpoint', 'Description',
                     'Memory', 'Runtime'),
                    ((function.get('function_id'),
                      function.get('name'),
                      function.get('endpoint'),
                      function.get('description'),
                      function.get('memory'),
                      function.get('runtime'),
                      ) for function in functions))


class FunctionDelete(Command):
    """Delete a function"""
    def get_parser(self, prog_name):
        parser = super(FunctionDelete, self).get_parser(prog_name)

        parser.add_argument(dest='function_id',
                            help='id of the function')

        return parser

    def take_action(self, parsed_args):
        self.app.client.functions.delete(parsed_args.function_id)


class FunctionExecute(Command):
    """Execute a function"""
    def get_parser(self, prog_name):
        parser = super(FunctionExecute, self).get_parser(prog_name)

        parser.add_argument(dest='function_id',
                            help='id of the function')

        parser.add_argument('--file',
                            dest='file',
                            required=True,
                            help='Path to json file with the payload')

        return parser

    def take_action(self, parsed_args):
        payload = utils.doc_from_json_file(parsed_args.file)
        e = self.app.client.functions.execute(parsed_args.function_id, payload)
        logging.info(e)


class FunctionRunningList(Lister):
    """List running functions"""
    def get_parser(self, prog_name):
        parser = super(FunctionRunningList, self).get_parser(prog_name)

        parser.add_argument(
            '--only-id',
            dest='only_id',
            default=False,
            action='store_true',
            help='Display only the Ids',
        )

        return parser

    def take_action(self, parsed_args):
        functions = self.app.client.functions.running_list()

        # TODO(m3m0): Show request_id
        if parsed_args.only_id:
            return (('Run ID',),
                    ((function.get('run_id'),) for function in functions))

        else:
            return (('Function ID', 'Run ID', 'Name', 'Time running',
                     'Memory', 'Runtime'),
                    ((function.get('function_id'),
                      function.get('name'),
                      function.get('endpoint'),
                      function.get('description'),
                      function.get('memory'),
                      function.get('runtime'),
                      ) for function in functions))
