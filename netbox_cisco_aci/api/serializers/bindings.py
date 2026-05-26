"""DRF serializers for Phase 6 binding models."""

import re

from dcim.api.serializers import InterfaceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ...models.bindings import (
    ACIDomainBinding,
    ACIInterfaceFabricMembership,
    ACIStaticPortBinding,
    ACIVPCBindingPair,
)
from .access import ACIDomainSerializer
from .fabric import ACINodeSerializer
from .tenant import ACIEndpointGroupSerializer


def _clean_name(value: str) -> str:
    """Strip APIC-illegal chars and cap at 64."""
    return re.sub(r"[^A-Za-z0-9._:\-]", "_", value)[:64]


class _AutoNameMixin:
    """Auto-derive ``name`` from FK fields when the client omits it.

    Bindings are uniquely identified by their FK relationships; APIC
    expects a name, so we synthesize a deterministic, APIC-safe value
    before ``full_clean()`` rejects the blank.
    """

    def _derive_name(self, attrs: dict) -> str:  # pragma: no cover - subclass override
        return ""

    def validate(self, data):
        # When used as a nested representation, ``data`` is already the resolved
        # related object — skip our auto-name logic entirely.
        if getattr(self, "nested", False):
            return super().validate(data)
        if not data.get("name"):
            # Build attrs view that includes the existing instance state for partial updates.
            merged = {}
            if self.instance is not None:
                for field in (
                    "aci_endpoint_group",
                    "dcim_interface",
                    "aci_domain",
                    "aci_node",
                    "binding_a",
                    "binding_b",
                    "encap_vlan",
                    "name",
                ):
                    if hasattr(self.instance, field):
                        merged[field] = getattr(self.instance, field)
            merged.update(data)
            derived = self._derive_name(merged)
            if derived:
                data["name"] = derived
            elif self.instance is not None and self.instance.name:
                # On partial update without enough info, retain existing name.
                data["name"] = self.instance.name
        return super().validate(data)


def _url(view: str):
    return serializers.HyperlinkedIdentityField(
        view_name=f"plugins-api:netbox_cisco_aci-api:{view}-detail"
    )


# ---------------------------------------------------------------------------
# ACIStaticPortBinding
# ---------------------------------------------------------------------------


class ACIStaticPortBindingSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acistaticportbinding")
    aci_endpoint_group = ACIEndpointGroupSerializer(nested=True)
    dcim_interface = InterfaceSerializer(nested=True)
    # Name is auto-derived from FKs by `_AutoNameMixin` if not provided.
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        epg = attrs.get("aci_endpoint_group")
        iface = attrs.get("dcim_interface")
        vlan = attrs.get("encap_vlan") or 0
        if not (epg and iface):
            return ""
        return _clean_name(f"spb_{getattr(epg, 'name', '')}_{iface}_v{vlan}")

    class Meta:
        model = ACIStaticPortBinding
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_endpoint_group",
            "dcim_interface",
            "binding_type",
            "encap_vlan",
            "mode",
            "primary_encap_vlan",
            "deployment_immediacy",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_endpoint_group",
            "binding_type",
            "dcim_interface",
            "description",
            "display",
            "encap_vlan",
            "id",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIVPCBindingPair
# ---------------------------------------------------------------------------


class ACIVPCBindingPairSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acivpcbindingpair")
    binding_a = ACIStaticPortBindingSerializer(nested=True)
    binding_b = ACIStaticPortBindingSerializer(nested=True)
    # Name is auto-derived from FKs by `_AutoNameMixin` if not provided.
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        a = attrs.get("binding_a")
        b = attrs.get("binding_b")
        if not (a and b):
            return ""
        return _clean_name(f"vpc_pair_{a.pk}_{b.pk}")

    class Meta:
        model = ACIVPCBindingPair
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "binding_a",
            "binding_b",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "binding_a",
            "binding_b",
            "description",
            "display",
            "id",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIDomainBinding
# ---------------------------------------------------------------------------


class ACIDomainBindingSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("acidomainbinding")
    aci_endpoint_group = ACIEndpointGroupSerializer(nested=True)
    aci_domain = ACIDomainSerializer(nested=True)
    # Name is auto-derived from FKs by `_AutoNameMixin` if not provided.
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        epg = attrs.get("aci_endpoint_group")
        dom = attrs.get("aci_domain")
        if not (epg and dom):
            return ""
        return _clean_name(f"dombnd_{getattr(epg, 'name', '')}_{getattr(dom, 'name', '')}")

    class Meta:
        model = ACIDomainBinding
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "aci_endpoint_group",
            "aci_domain",
            "deployment_immediacy",
            "resolution_immediacy",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_domain",
            "aci_endpoint_group",
            "description",
            "display",
            "id",
            "url",
        )


# ---------------------------------------------------------------------------
# ACIInterfaceFabricMembership
# ---------------------------------------------------------------------------


class ACIInterfaceFabricMembershipSerializer(_AutoNameMixin, NetBoxModelSerializer):
    url = _url("aciinterfacefabricmembership")
    dcim_interface = InterfaceSerializer(nested=True)
    aci_node = ACINodeSerializer(nested=True)
    # Name is auto-derived from FKs by `_AutoNameMixin` if not provided.
    name = serializers.CharField(required=False, allow_blank=True, max_length=64)

    def _derive_name(self, attrs: dict) -> str:
        node = attrs.get("aci_node")
        iface = attrs.get("dcim_interface")
        if not (node and iface):
            return ""
        return _clean_name(f"ifm_{getattr(node, 'name', '')}_{iface}")

    class Meta:
        model = ACIInterfaceFabricMembership
        fields = (
            "id",
            "url",
            "display",
            "name",
            "name_alias",
            "dcim_interface",
            "aci_node",
            "interface_role",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "aci_node",
            "dcim_interface",
            "description",
            "display",
            "id",
            "interface_role",
            "url",
        )
