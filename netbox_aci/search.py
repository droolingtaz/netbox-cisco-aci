"""SearchIndex registrations for the global NetBox search."""

from netbox.search import SearchIndex, register_search

from .models.fabric import ACIFabric, ACINode, ACIPod


@register_search
class ACIFabricIndex(SearchIndex):
    model = ACIFabric
    fields = (
        ("name", 100),
        ("description", 500),
        ("fabric_id", 100),
    )


@register_search
class ACIPodIndex(SearchIndex):
    model = ACIPod
    fields = (
        ("name", 100),
        ("description", 500),
        ("pod_id", 100),
    )


@register_search
class ACINodeIndex(SearchIndex):
    model = ACINode
    fields = (
        ("name", 100),
        ("description", 500),
        ("node_id", 100),
        ("serial_number", 200),
    )
