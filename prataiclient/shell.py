import logging

import os
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from prataiclient.v1 import clusters
from prataiclient.v1 import events
from prataiclient.v1 import images
from prataiclient.v1 import functions
from prataiclient.v1.client import Client

LOG = logging.getLogger(__name__)


class PrataiCommandManager(CommandManager):
    """ All commands available for the shell are registered here """
    SHELL_COMMANDS = {
        'function-create': functions.FunctionCreate,
        'function-list': functions.FunctionList,
        'function-show': functions.FunctionShow,
        'function-delete': functions.FunctionDelete,
        'function-execute': functions.FunctionExecute,
        'function-running': functions.FunctionRunningList,
        'runtime-list': images.ImageList,
        'runtime-show': images.ImageShow,
        'cluster-status': clusters.ClusterStatus,
        'event-list': events.EventList,
        'event-show': events.EventShow
    }

    def load_commands(self, namespace):
        for name, command_class in self.SHELL_COMMANDS.items():
            self.add_command(name, command_class)


class PrataiShell(App):
    def __init__(self):
        super(PrataiShell, self).__init__(
            description='Python Pratai Client',
            version='0.1',
            deferred_help=True,
            command_manager=PrataiCommandManager(None),
        )

    def build_option_parser(self, description, version):
        parser = super(PrataiShell, self).build_option_parser(description,
                                                              version)
        parser.add_argument(
            '--os-auth-url',
            dest='os_auth_url',
            default=os.environ.get('OS_AUTH_URL'),
            help='Specify identity endpoint',
        )

        parser.add_argument(
            '--os-pratai-url',
            dest='os_pratai_url',
            default=os.environ.get('OS_PRATAI_URL'),
            help='Specify the Pratai service endpoint to use'
        )

        parser.add_argument(
            '--os-endpoint-type',
            dest='os_endpoint_type',
            default=os.environ.get('OS_ENDPOINT_TYPE'),
            help='''Endpoint type to select. Valid endpoint types:
                    "public" or "publicURL", "internal" or "internalURL",
                    "admin" or "adminURL"'''
        )

        parser.add_argument(
            '--os-identity-api-version',
            dest='os_identity_api_version',
            default=os.environ.get('OS_IDENTITY_API_VERSION'),
            help='Identity API version: 2.0 or 3'
        )

        parser.add_argument(
            '--os-password',
            dest='os_password',
            default=os.environ.get('OS_PASSWORD'),
            help='''Password used for authentication with the OpenStack
                    Identity service'''
        )

        parser.add_argument(
            '--os-username',
            dest='os_username',
            default=os.environ.get('OS_USERNAME'),
            help='''Name used for authentication with the OpenStack
                    Identity service'''
        )

        parser.add_argument(
            '--os-token',
            dest='os_token',
            default=os.environ.get('OS_TOKEN'),
            help='''Specify an existing token to use instead of retrieving
                    one via authentication'''
        )

        parser.add_argument(
            '--os-project-domain-name',
            dest='os_project_domain_name',
            default=os.environ.get('OS_PROJECT_DOMAIN_NAME'),
            help='Domain name containing project'
        )

        parser.add_argument(
            '--os-project-name',
            dest='os_project_name',
            default=os.environ.get('OS_PROJECT_NAME'),
            help='Project name to scope to'
        )

        parser.add_argument(
            '--os-region-name',
            dest='os_region_name',
            default=os.environ.get('OS_REGION_NAME'),
            help='Specify the region to use'
        )

        parser.add_argument(
            '--os-tenant-id',
            dest='os_tenant_id',
            default=os.environ.get('OS_TENANT_ID'),
            help='Tenant to request authorization on'
        )

        parser.add_argument(
            '--os-tenant-name',
            dest='os_tenant_name',
            default=os.environ.get('OS_TENANT_NAME'),
            help='Tenant to request authorization on'
        )

        parser.add_argument(
            '--os-user-domain-name',
            dest='os_user_domain_name',
            default=os.environ.get('OS_USER_DOMAIN_NAME'),
            help='User domain name'
        )

        parser.add_argument(
            '-k', '--insecure',
            dest='insecure',
            action='store_true',
            default=os.environ.get('OS_INSECURE'),
            help='use python-prataiclient with insecure connections'
        )

        parser.add_argument(
            '--os-cacert',
            dest='os_cacert',
            default=os.environ.get('OS_CACERT'),
            help='''Path of CA TLS certificate(s) used to verify the
                    remote server's certificate. Without this option
                    pratai looks for the default system CA certificates.'''
        )

        parser.add_argument(
            '--os-cert',
            dest='os_cert',
            default=os.environ.get('OS_CERT'),
            help='''Path of CERT TLS certificate(s) used to verify the
                    remote server's certificate.1'''
        )

        return parser


    @property
    def client(self):
        """ Build a client object to communicate with the API
        :return: freezerclient object
        """
        opts = {
            'token': self.options.os_token,
            'version': self.options.os_identity_api_version,
            'username': self.options.os_username,
            'password': self.options.os_password,
            'tenant_name': self.options.os_tenant_name,
            'auth_url': self.options.os_auth_url,
            'endpoint': self.options.os_pratai_url,
            'project_name': self.options.os_project_name,
            'user_domain_name': self.options.os_user_domain_name,
            'project_domain_name': self.options.os_project_domain_name,
            'verify': True or self.options.os_cacert,
            'cert': self.options.os_cert
        }
        return Client(**opts)


def main(argv=sys.argv[1:]):
    """Starts the main application"""
    return PrataiShell().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
