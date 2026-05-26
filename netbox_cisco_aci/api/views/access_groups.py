"""DRF ViewSet for Interface Policy Groups (Phase 4)."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.access_groups import ACIInterfacePolicyGroupFilterSet
from ...models.access import ACIInterfacePolicyGroup
from ..serializers.access_groups import ACIInterfacePolicyGroupSerializer


class ACIInterfacePolicyGroupViewSet(NetBoxModelViewSet):
    queryset = ACIInterfacePolicyGroup.objects.select_related(
        "aci_fabric",
        "link_level_policy",
        "cdp_policy",
        "lldp_policy",
        "lacp_policy",
        "mcp_policy",
        "stp_policy",
        "aaep",
    )
    serializer_class = ACIInterfacePolicyGroupSerializer
    filterset_class = ACIInterfacePolicyGroupFilterSet
