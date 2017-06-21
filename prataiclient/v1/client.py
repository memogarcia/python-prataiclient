import os

from prataiclient.utils import CachedProperty
from prataiclient.utils import Namespace
from prataiclient.v1.managers import functions
from prataiclient.v1.managers import images
from prataiclient.v1.managers import clusters
from prataiclient.v1.managers import events

from keystoneclient.auth.identity import v2
from keystoneclient.auth.identity import v3
from keystoneclient import session as ksc_session


def guess_auth_version(opts):
    """ Guess keystone version to connect to"""
    if opts.os_identity_api_version == '3':
        return '3'
    elif opts.os_identity_api_version == '2.0':
        return '2.0'
    elif opts.os_auth_url.endswith('v3'):
        return '3'
    elif opts.os_auth_url.endswith('v2.0'):
        return '2.0'
    raise Exception('Please provide valid keystone auth url with valid'
                    ' keystone api version to use')


def get_auth_plugin(opts):
    """Create the right keystone connection depending on the version
    for the api, if username/password and token are provided, username and
    password takes precedence.
    """
    auth_version = guess_auth_version(opts)
    if opts.os_username:
        if auth_version == '3':
            return v3.Password(auth_url=opts.os_auth_url,
                               username=opts.os_username,
                               password=opts.os_password,
                               project_name=opts.os_project_name,
                               user_domain_name=opts.os_user_domain_name,
                               project_domain_name=opts.os_project_domain_name)
        elif auth_version == '2.0':
            return v2.Password(auth_url=opts.os_auth_url,
                               username=opts.os_username,
                               password=opts.os_password,
                               tenant_name=opts.os_tenant_name)
    elif opts.os_token:
        if auth_version == '3':
            return v3.Token(auth_url=opts.os_auth_url,
                            token=opts.os_token,
                            project_name=opts.os_project_name,
                            project_domain_name=opts.os_project_domain_name)
        elif auth_version == '2.0':
            return v2.Token(auth_url=opts.os_auth_url,
                            token=opts.os_token,
                            tenant_name=opts.os_tenant_name)
    raise Exception('Unable to determine correct auth method, please provide'
                    ' either username or token')


class Client(object):
    """Client for the OpenStack Disaster Recovery v1 API.
    """

    def __init__(self, version='3', token=None, username=None, password=None,
                 tenant_name=None, auth_url=None, session=None, endpoint=None,
                 opts=None, project_name=None, user_domain_name=None,
                 project_domain_name=None, verify=True, cert=None):
        """
        Initialize a new client for the Disaster Recovery v1 API.
        :param version: keystone version to use
        :param token: keystone token
        :param username: openstack username
        :param password: openstack password
        :param tenant_name: tenant
        :param auth_url: keystone-api endpoint
        :param session: keystone.Session
        :param endpoint: freezer-api endpoint
        :param opts: a namespace to store all keystone data
        :param project_name: only for version 3
        :param user_domain_name: only for version 3
        :param project_domain_name: only for version 3
        :param verify: The verification arguments to pass to requests.
                       These are of the same form as requests expects,
                       so True or False to verify (or not) against system
                       certificates or a path to a bundle or CA certs to
                       check against or None for requests to
                       attempt to locate and use certificates. (optional,
                       defaults to True)
        :param cert: Path to cert
        :return: freezerclient.Client
        """
        self.opts = opts or Namespace({})
        self.opts.os_token = token or None
        self.opts.os_username = username or None
        self.opts.os_password = password or None
        self.opts.os_tenant_name = tenant_name or None
        self.opts.os_auth_url = auth_url or None
        self.opts.os_backup_url = endpoint or None
        self.opts.os_project_name = project_name or None
        self.opts.os_user_domain_name = user_domain_name or None
        self.opts.os_project_domain_name = project_domain_name or None
        self.opts.auth_version = version
        self.verify = verify
        self.cert = cert
        #self._session = session
        self.endpoint = endpoint

        self.validate()

        self.events = events.EventManager(self, verify=verify)
        self.cluster = clusters.ClusterManager(self, verify=verify)
        self.images = images.ImageManager(self, verify=verify)
        self.functions = functions.FunctionManager(self, verify=verify)

    '''
    @CachedProperty
    def session(self):
        if self._session:
            return self._session
        auth_plugin = get_auth_plugin(self.opts)
        return ksc_session.Session(auth=auth_plugin,
                                   verify=self.verify,
                                   cert=self.cert)
    '''
    @property
    def auth_token(self):
        #return self.session.get_token()
        return ''

    def validate(self):
        pratai_url = os.environ.get('OS_PRATAI_URL', None)
        if not pratai_url:
            raise Exception('No OS_PRATAI_URL set up')
