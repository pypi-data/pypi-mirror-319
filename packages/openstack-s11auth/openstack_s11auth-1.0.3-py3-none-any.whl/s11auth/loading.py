from keystoneauth1 import loading

from s11auth import plugin


class S11Auth(loading.BaseLoader):
    plugin_class = plugin.S11Auth

    def get_options(self):
        return [
            loading.Opt('auth-url', help='The URL of Keystone', default='https://keystone.cloud.syseleven.net:5000/v3'),
            loading.Opt('project-id', help='Project ID to scope to'),
            loading.Opt('redirect-port', help='Port to listen on for redirect', default='8080'),
        ]
