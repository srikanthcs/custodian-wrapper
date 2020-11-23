
from c7n.resources.ec2 import actions as ec2_actions
from c7n.resources.elb import actions as elb_actions

# from .custom_actions.log2clp import Log2Clp
from custom_actions.log2clp import Log2Clp

resource_actions = (ec2_actions, elb_actions)


def register_custom_actions():

    # ec2_plugins = PluginRegistry("ec2.actions")
    # print(ec2_plugins)
    # ec2_plugins.register('log2clp_v2', Log2Clp)
    for resource in resource_actions:
        resource.register('log2clp_v2', Log2Clp)

    # ec2_actions.register('log2clp_v2', Log2Clp)
    # elb_actions.register('log2clp_v2', Log2Clp)
    # print(ec2_actions)
    # print(ec2_actions._factories)
    # print(ec2_actions._subscribers)

