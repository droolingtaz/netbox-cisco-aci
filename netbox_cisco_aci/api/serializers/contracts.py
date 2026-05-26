"""DRF serializers for Phase 5 contract / filter / relation models."""

from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from .tenant import (
    ACIEndpointGroupSerializer,
    ACIEndpointSecurityGroupSerializer,
    ACITenantSerializer,
)


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# ACIContract
# ---------------------------------------------------------------------------


class ACIContractSerializer(NetBoxModelSerializer):
    url = _url("acicontract")
    aci_tenant = ACITenantSerializer(nested=True)

    class Meta:
        model = ACIContract
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "scope",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "scope",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIFilter
# ---------------------------------------------------------------------------


class ACIFilterSerializer(NetBoxModelSerializer):
    url = _url("acifilter")
    aci_tenant = ACITenantSerializer(nested=True)

    class Meta:
        model = ACIFilter
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_tenant",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_tenant",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIFilterEntry
# ---------------------------------------------------------------------------


class ACIFilterEntrySerializer(NetBoxModelSerializer):
    url = _url("acifilterentry")
    aci_filter = ACIFilterSerializer(nested=True)

    class Meta:
        model = ACIFilterEntry
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_filter",
            "ether_type",
            "ip_protocol",
            "source_port_from",
            "source_port_to",
            "destination_port_from",
            "destination_port_to",
            "tcp_rules",
            "match_only_fragments",
            "arp_opcode",
            "stateful",
            "icmp_v4_type",
            "icmp_v6_type",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_filter",
            "description",
            "display",
            "ether_type",
            "id",
            "ip_protocol",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACISubject
# ---------------------------------------------------------------------------


class ACISubjectSerializer(NetBoxModelSerializer):
    url = _url("acisubject")
    aci_contract = ACIContractSerializer(nested=True)

    class Meta:
        model = ACISubject
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_contract",
            "apply_both_directions",
            "reverse_filter_ports",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_contract",
            "description",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACISubjectFilter (through-model)
# ---------------------------------------------------------------------------


class ACISubjectFilterSerializer(NetBoxModelSerializer):
    url = _url("acisubjectfilter")
    aci_subject = ACISubjectSerializer(nested=True)
    aci_filter = ACIFilterSerializer(nested=True)

    class Meta:
        model = ACISubjectFilter
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_subject",
            "aci_filter",
            "direction",
            "action",
            "priority",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_filter",
            "aci_subject",
            "description",
            "direction",
            "display",
            "id",
            "name",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIContractRelation
# ---------------------------------------------------------------------------


class ACIContractRelationSerializer(NetBoxModelSerializer):
    url = _url("acicontractrelation")
    aci_contract = ACIContractSerializer(nested=True)
    aci_endpoint_group = ACIEndpointGroupSerializer(nested=True, required=False, allow_null=True)
    aci_endpoint_security_group = ACIEndpointSecurityGroupSerializer(
        nested=True, required=False, allow_null=True
    )

    class Meta:
        model = ACIContractRelation
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_contract",
            "aci_endpoint_group",
            "aci_endpoint_security_group",
            "role",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_contract",
            "description",
            "display",
            "id",
            "name",
            "role",
            "url",
        )
