from c7n.provider import import_resource_classes
from custodian_v2.custom_actions.log2clp import Log2Clp
from c7n.provider import clouds

def register_custom_actions():
    provider = clouds.get("aws")
    # print(provider.resource_map)
    resource_classes, not_found = import_resource_classes(
        provider.resource_map, '*')
    # print(resource_classes, not_found)

    for resource in resource_classes:
        # print(resource.action_registry._factories)
        resource.action_registry.register('log2clp_v2', Log2Clp)
