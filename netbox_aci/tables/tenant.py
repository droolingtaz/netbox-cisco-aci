"""Tables for tenancy models."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.tenant import (
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
    ACIVRF,
)


class ACITenantTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_fabric = tables.Column(linkify=True, verbose_name="Fabric")
    vrf_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_aci:acivrf_list",
        url_params={"aci_tenant_id": "pk"},
        verbose_name="VRFs",
    )
    bd_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_aci:acibridgedomain_list",
        url_params={"aci_tenant_id": "pk"},
        verbose_name="BDs",
    )
    app_profile_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_aci:aciappprofile_list",
        url_params={"aci_tenant_id": "pk"},
        verbose_name="APs",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_aci:acitenant_list")

    class Meta(NetBoxTable.Meta):
        model = ACITenant
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_fabric",
            "vrf_count",
            "bd_count",
            "app_profile_count",
            "description",
            "tags",
            "created",
            "last_updated",
        )
        default_columns = (
            "name",
            "aci_fabric",
            "vrf_count",
            "bd_count",
            "app_profile_count",
            "description",
        )


class ACIVRFTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    nb_vrf = tables.Column(linkify=True, verbose_name="NetBox VRF")
    policy_enforcement_preference = ChoiceFieldColumn(verbose_name="Pol enforcement")
    policy_enforcement_direction = ChoiceFieldColumn(verbose_name="Direction")
    tags = columns.TagColumn(url_name="plugins:netbox_aci:acivrf_list")

    class Meta(NetBoxTable.Meta):
        model = ACIVRF
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "nb_vrf",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_tenant",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "preferred_group_enabled",
        )


class ACIBridgeDomainTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    aci_vrf = tables.Column(linkify=True, verbose_name="VRF")
    unicast_routing_enabled = columns.BooleanColumn(verbose_name="Unicast routing")
    limit_ip_learn_to_subnets = columns.BooleanColumn(verbose_name="Limit IP learn")
    l2_unknown_unicast = ChoiceFieldColumn(verbose_name="L2 unk-uc")
    subnet_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_aci:acibridgedomainsubnet_list",
        url_params={"aci_bridge_domain_id": "pk"},
        verbose_name="Subnets",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_aci:acibridgedomain_list")

    class Meta(NetBoxTable.Meta):
        model = ACIBridgeDomain
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_vrf",
            "unicast_routing_enabled",
            "limit_ip_learn_to_subnets",
            "l2_unknown_unicast",
            "subnet_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_tenant",
            "aci_vrf",
            "unicast_routing_enabled",
            "subnet_count",
        )


class ACIBridgeDomainSubnetTable(NetBoxTable):
    aci_bridge_domain = tables.Column(linkify=True, verbose_name="Bridge Domain")
    gateway_ip = tables.Column(linkify=True, verbose_name="Gateway IP")
    nb_prefix = tables.Column(linkify=True, verbose_name="NetBox prefix")
    is_primary = columns.BooleanColumn(verbose_name="Primary")
    tags = columns.TagColumn(url_name="plugins:netbox_aci:acibridgedomainsubnet_list")

    class Meta(NetBoxTable.Meta):
        model = ACIBridgeDomainSubnet
        fields = (
            "pk",
            "id",
            "aci_bridge_domain",
            "gateway_ip",
            "nb_prefix",
            "scope_public",
            "scope_shared",
            "scope_private",
            "is_primary",
            "description",
            "tags",
        )
        default_columns = (
            "aci_bridge_domain",
            "gateway_ip",
            "scope_public",
            "scope_shared",
            "is_primary",
        )


class ACIAppProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    epg_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_aci:aciendpointgroup_list",
        url_params={"aci_app_profile_id": "pk"},
        verbose_name="EPGs",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_aci:aciappprofile_list")

    class Meta(NetBoxTable.Meta):
        model = ACIAppProfile
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "epg_count",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_tenant", "epg_count", "description")


class ACIEndpointGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    aci_app_profile = tables.Column(linkify=True, verbose_name="App Profile")
    aci_bridge_domain = tables.Column(linkify=True, verbose_name="BD")
    is_useg = columns.BooleanColumn(verbose_name="uSeg")
    admin_shutdown = columns.BooleanColumn(verbose_name="Shutdown")
    qos_class = ChoiceFieldColumn(verbose_name="QoS")
    tags = columns.TagColumn(url_name="plugins:netbox_aci:aciendpointgroup_list")

    class Meta(NetBoxTable.Meta):
        model = ACIEndpointGroup
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_app_profile",
            "aci_bridge_domain",
            "is_useg",
            "admin_shutdown",
            "intra_epg_isolation",
            "preferred_group_member",
            "qos_class",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_app_profile",
            "aci_bridge_domain",
            "is_useg",
            "qos_class",
        )


class ACIUSegAttributeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_endpoint_group = tables.Column(linkify=True, verbose_name="EPG")
    attribute_type = ChoiceFieldColumn(verbose_name="Type")
    match_operator = ChoiceFieldColumn(verbose_name="Operator")
    match_value = tables.Column(verbose_name="Value")
    tags = columns.TagColumn(url_name="plugins:netbox_aci:aciusegattribute_list")

    class Meta(NetBoxTable.Meta):
        model = ACIUSegAttribute
        fields = (
            "pk",
            "id",
            "name",
            "aci_endpoint_group",
            "attribute_type",
            "match_operator",
            "match_value",
            "description",
            "tags",
        )
        default_columns = (
            "aci_endpoint_group",
            "attribute_type",
            "match_operator",
            "match_value",
        )


class ACIEndpointSecurityGroupTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    aci_vrf = tables.Column(linkify=True, verbose_name="VRF")
    aci_app_profile = tables.Column(linkify=True, verbose_name="App Profile")
    admin_shutdown = columns.BooleanColumn(verbose_name="Shutdown")
    qos_class = ChoiceFieldColumn(verbose_name="QoS")
    tags = columns.TagColumn(url_name="plugins:netbox_aci:aciendpointsecuritygroup_list")

    class Meta(NetBoxTable.Meta):
        model = ACIEndpointSecurityGroup
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "aci_vrf",
            "aci_app_profile",
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "qos_class",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_tenant", "aci_vrf", "qos_class")
