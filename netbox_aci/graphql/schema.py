"""Strawberry GraphQL schema for the plugin.

Each model gets a type plus a `list_*` resolver and a `*` (single-object)
resolver. NetBox merges this schema into its own at startup.
"""

from typing import Optional

import strawberry
import strawberry_django
from strawberry import auto

from ..models.fabric import ACIFabric, ACINode, ACIPod


@strawberry_django.type(ACIFabric, fields="__all__")
class ACIFabricType:
    pass


@strawberry_django.type(ACIPod, fields="__all__")
class ACIPodType:
    pass


@strawberry_django.type(ACINode, fields="__all__")
class ACINodeType:
    pass


@strawberry.type
class Query:
    aci_fabric: Optional[ACIFabricType] = strawberry_django.field()
    aci_fabric_list: list[ACIFabricType] = strawberry_django.field()

    aci_pod: Optional[ACIPodType] = strawberry_django.field()
    aci_pod_list: list[ACIPodType] = strawberry_django.field()

    aci_node: Optional[ACINodeType] = strawberry_django.field()
    aci_node_list: list[ACINodeType] = strawberry_django.field()

    # `auto` is imported to keep parity with NetBox plugin examples even
    # though it is not directly referenced in the resolvers above.
    _auto: Optional[strawberry.Private[type(auto)]] = None


schema = [Query]
