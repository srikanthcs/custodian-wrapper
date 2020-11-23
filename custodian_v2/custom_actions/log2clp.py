# Copyright 2019 Microsoft Corporation
# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

try:
    import certifi
except ImportError:
    certifi = None

import jmespath

import urllib3
from urllib import parse

from c7n import utils
from c7n.actions.core import EventAction


class Log2Clp(EventAction):
    """Calls a webhook with optional parameters and body
       populated from JMESPath queries.

        .. code-block:: yaml

          policies:
            - name: call-webhook
              resource: ec2
              description: |
                Call webhook with list of resource groups
              actions:
               - type: webhook
                 url: http://foo.com
                 query-params:
                    resource_name: resource.name
                    policy_name: policy.name
    """

    schema_alias = True
    schema = utils.type_schema(
        'log2clp_v2',
        required=['url'],
        **{
            'url': {'type': 'string'},
            'body': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'string'
                    }
                },
            'batch': {'type': 'boolean'},
            'batch-size': {'type': 'number'},
            'method': {'type': 'string', 'enum': ['PUT', 'POST', 'GET', 'PATCH', 'DELETE']},
            'query-params': {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "query string values"
                }
            },
            'headers': {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "header values"
                }
            }
        }
    )

    def __init__(self, data=None, manager=None, log_dir=None):
        super(Log2Clp, self).__init__(data, manager, log_dir)
        self.http = None
        self.url = self.data.get('url')
        self.body = self.data.get('body', {})
        self.batch = self.data.get('batch', False)
        self.batch_size = self.data.get('batch-size', 500)
        self.query_params = self.data.get('query-params', {})
        self.headers = self.data.get('headers', {})
        self.method = self.data.get('method', 'POST')
        self.lookup_data = None

    def process(self, resources, event=None):
        self.lookup_data = {
            'account_id': self.manager.config.account_id,
            'region': self.manager.config.region,
            'execution_id': self.manager.ctx.execution_id,
            'execution_start': self.manager.ctx.start_time,
            'policy': self.manager.data
        }

        self.http = self._build_http_manager()

        if self.batch:
            for chunk in utils.chunks(resources, self.batch_size):
                resource_data = self.lookup_data
                resource_data['resources'] = chunk
                self._process_call(resource_data)
        else:
            for r in resources:
                resource_data = self.lookup_data
                resource_data['resource'] = r
                self._process_call(resource_data)

    def _process_call(self, resource):

        self.log.info(resource)

        prepared_url = self._build_url(resource)
        prepared_body = self._build_body(resource)
        prepared_headers = self._build_headers(resource)

        if prepared_body:
            prepared_headers['content-type'] = 'application/json'

        self.log.info(prepared_url)
        self.log.info(prepared_headers)
        self.log.info(prepared_body)

        try:
            import requests
            res = requests.post(
                # method=self.method,
                url=prepared_url,
                data=prepared_body,
                headers=prepared_headers,
                verify=False)

            self.log.info("%s got response %s with URL %s" %
                          (self.method, res.status_code, prepared_url))
            self.log.info(res.reason)
            self.log.info(res.text)
        except urllib3.exceptions.HTTPError as e:
            self.log.error("Error calling %s. Code: %s" % (prepared_url, e.reason))

    def _build_http_manager(self):
        pass
        # pool_kwargs = {
        #     'cert_reqs': 'CERT_REQUIRED',
        #     'ca_certs': certifi and certifi.where() or None
        # }
        #
        # proxy_url = utils.get_proxy_url(self.url)
        # if proxy_url:
        #     return urllib3.ProxyManager(proxy_url, **pool_kwargs)
        # else:
        #     return urllib3.PoolManager(**pool_kwargs)


    def _build_headers(self, resource):
        return self.headers

    def _build_url(self, resource):
        """
        Compose URL with query string parameters.

        Will not lose existing static parameters in the URL string
        but does not support 'duplicate' parameter entries
        """

        if not self.query_params:
            return self.url

        evaluated_params = {k: jmespath.search(v, resource) for k, v in self.query_params.items()}

        url_parts = list(parse.urlparse(self.url))
        query = dict(parse.parse_qsl(url_parts[4]))
        query.update(evaluated_params)
        url_parts[4] = parse.urlencode(query)

        return parse.urlunparse(url_parts)

    def _build_body(self, resource):
        """Create a JSON body and dump it to encoded bytes."""

        if not self.body:
            return None
        # self.log.info(self.body)
        prep_prop = {}
        for _key in self.body:
            try:
                prep_prop[_key] = jmespath.search(self.body[_key], resource)
                if not prep_prop[_key]:
                    if resource["policy"]["resource"] == 's3' and self.body[_key] == "resource.Location.LocationConstraint":
                        prep_prop[_key] = "us-east-1"
                    else:
                        prep_prop[_key] = self.body[_key]
            except:
                prep_prop[_key] = self.body[_key]

        self.log.info([prep_prop])
        return utils.dumps([prep_prop])

