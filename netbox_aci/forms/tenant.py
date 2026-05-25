"""Forms for tenancy models."""

from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from ..choices import (
    BDL2UnknownUnicastChoices,
    BDL3UnknownMulticastChoices,
    BDMultiDestinationChoices,
    QualityOfServiceClassChoices,
    USegAttributeMatchOperatorChoices,
    USegAttributeTypeChoices,
    VRFPolicyEnforcementChoices,
    VRFPolicyEnforcementPreferenceChoices,
)
from ..models.fabric import ACIFabric
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


# ---------------------------------------------------------------------------
# ACITenant
# ---------------------------------------------------------------------------

class ACITenantForm(NetBoxModelForm):
    aci_fabric = DynamicModelChoiceField(queryset=ACIFabric.objects.all(), label=_("Fabric"))
    fieldsets = (
        FieldSet("aci_fabric", "name", "name_alias", "description", name=_("Tenant")),
    )

    class Meta:
        model = ACITenant
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


class ACITenantBulkEditForm(NetBoxModelBulkEditForm):
    model = ACITenant
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACITenantFilterForm(NetBoxModelFilterSetForm):
    model = ACITenant
    aci_fabric_id = DynamicModelMultipleChoiceField(
        queryset=ACIFabric.objects.all(), required=False, label=_("Fabric")
    )


class ACITenantImportForm(NetBoxModelImportForm):
    aci_fabric = forms.ModelChoiceField(queryset=ACIFabric.objects.all(), to_field_name="name")

    class Meta:
        model = ACITenant
        fields = ("aci_fabric", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# ACIVRF
# ---------------------------------------------------------------------------

class ACIVRFForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    fieldsets = (
        FieldSet(
            "aci_tenant",
            "name",
            "name_alias",
            "nb_vrf",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
            name=_("VRF"),
        ),
    )

    class Meta:
        model = ACIVRF
        fields = (
            "aci_tenant",
            "name",
            "name_alias",
            "nb_vrf",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
            "tags",
        )


class ACIVRFBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIVRF
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), required=False)
    policy_enforcement_preference = forms.ChoiceField(
        choices=VRFPolicyEnforcementPreferenceChoices, required=False
    )
    policy_enforcement_direction = forms.ChoiceField(
        choices=VRFPolicyEnforcementChoices, required=False
    )
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIVRFFilterForm(NetBoxModelFilterSetForm):
    model = ACIVRF
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )


class ACIVRFImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")

    class Meta:
        model = ACIVRF
        fields = (
            "aci_tenant",
            "name",
            "name_alias",
            "policy_enforcement_preference",
            "policy_enforcement_direction",
            "bd_enforcement_enabled",
            "preferred_group_enabled",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIBridgeDomain
# ---------------------------------------------------------------------------

class ACIBridgeDomainForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    aci_vrf = DynamicModelChoiceField(
        queryset=ACIVRF.objects.all(),
        label=_("VRF"),
        query_params={"aci_tenant_id": "$aci_tenant"},
    )
    fieldsets = (
        FieldSet(
            "aci_tenant",
            "aci_vrf",
            "name",
            "name_alias",
            "description",
            name=_("Bridge Domain"),
        ),
        FieldSet(
            "unicast_routing_enabled",
            "arp_flooding_enabled",
            "limit_ip_learn_to_subnets",
            "l2_unknown_unicast",
            "l3_unknown_multicast",
            "multi_destination_flooding",
            "mac_address",
            name=_("L2 / L3 forwarding"),
        ),
    )

    class Meta:
        model = ACIBridgeDomain
        fields = (
            "aci_tenant",
            "aci_vrf",
            "name",
            "name_alias",
            "description",
            "unicast_routing_enabled",
            "arp_flooding_enabled",
            "limit_ip_learn_to_subnets",
            "l2_unknown_unicast",
            "l3_unknown_multicast",
            "multi_destination_flooding",
            "mac_address",
            "tags",
        )


class ACIBridgeDomainBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIBridgeDomain
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), required=False)
    aci_vrf = DynamicModelChoiceField(queryset=ACIVRF.objects.all(), required=False)
    unicast_routing_enabled = forms.NullBooleanField(required=False)
    limit_ip_learn_to_subnets = forms.NullBooleanField(required=False)
    l2_unknown_unicast = forms.ChoiceField(choices=BDL2UnknownUnicastChoices, required=False)
    l3_unknown_multicast = forms.ChoiceField(choices=BDL3UnknownMulticastChoices, required=False)
    multi_destination_flooding = forms.ChoiceField(
        choices=BDMultiDestinationChoices, required=False
    )
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "mac_address")


class ACIBridgeDomainFilterForm(NetBoxModelFilterSetForm):
    model = ACIBridgeDomain
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    aci_vrf_id = DynamicModelMultipleChoiceField(
        queryset=ACIVRF.objects.all(), required=False, label=_("VRF")
    )


class ACIBridgeDomainImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    aci_vrf = forms.ModelChoiceField(queryset=ACIVRF.objects.all(), to_field_name="name")

    class Meta:
        model = ACIBridgeDomain
        fields = (
            "aci_tenant",
            "aci_vrf",
            "name",
            "name_alias",
            "description",
            "unicast_routing_enabled",
            "arp_flooding_enabled",
            "limit_ip_learn_to_subnets",
            "l2_unknown_unicast",
            "l3_unknown_multicast",
            "multi_destination_flooding",
            "mac_address",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIBridgeDomainSubnet
# ---------------------------------------------------------------------------

class ACIBridgeDomainSubnetForm(NetBoxModelForm):
    aci_bridge_domain = DynamicModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(), label=_("Bridge Domain")
    )
    fieldsets = (
        FieldSet(
            "aci_bridge_domain",
            "name",
            "name_alias",
            "gateway_ip",
            "nb_prefix",
            "is_primary",
            "description",
            name=_("Subnet"),
        ),
        FieldSet(
            "scope_public",
            "scope_shared",
            "scope_private",
            name=_("Scope"),
        ),
    )

    class Meta:
        model = ACIBridgeDomainSubnet
        fields = (
            "aci_bridge_domain",
            "name",
            "name_alias",
            "gateway_ip",
            "nb_prefix",
            "scope_public",
            "scope_shared",
            "scope_private",
            "is_primary",
            "description",
            "tags",
        )


class ACIBridgeDomainSubnetBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIBridgeDomainSubnet
    aci_bridge_domain = DynamicModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(), required=False
    )
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIBridgeDomainSubnetFilterForm(NetBoxModelFilterSetForm):
    model = ACIBridgeDomainSubnet
    aci_bridge_domain_id = DynamicModelMultipleChoiceField(
        queryset=ACIBridgeDomain.objects.all(), required=False, label=_("Bridge Domain")
    )


class ACIBridgeDomainSubnetImportForm(NetBoxModelImportForm):
    aci_bridge_domain = forms.ModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACIBridgeDomainSubnet
        fields = (
            "aci_bridge_domain",
            "name",
            "name_alias",
            "gateway_ip",
            "scope_public",
            "scope_shared",
            "scope_private",
            "is_primary",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIAppProfile
# ---------------------------------------------------------------------------

class ACIAppProfileForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    fieldsets = (
        FieldSet(
            "aci_tenant",
            "name",
            "name_alias",
            "description",
            name=_("Application Profile"),
        ),
    )

    class Meta:
        model = ACIAppProfile
        fields = ("aci_tenant", "name", "name_alias", "description", "tags")


class ACIAppProfileBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIAppProfile
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIAppProfileFilterForm(NetBoxModelFilterSetForm):
    model = ACIAppProfile
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )


class ACIAppProfileImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")

    class Meta:
        model = ACIAppProfile
        fields = ("aci_tenant", "name", "name_alias", "description", "tags")


# ---------------------------------------------------------------------------
# ACIEndpointGroup
# ---------------------------------------------------------------------------

class ACIEndpointGroupForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    aci_app_profile = DynamicModelChoiceField(
        queryset=ACIAppProfile.objects.all(),
        label=_("App Profile"),
        query_params={"aci_tenant_id": "$aci_tenant"},
    )
    aci_bridge_domain = DynamicModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(),
        label=_("Bridge Domain"),
    )

    fieldsets = (
        FieldSet(
            "aci_tenant",
            "aci_app_profile",
            "aci_bridge_domain",
            "name",
            "name_alias",
            "description",
            name=_("Endpoint Group"),
        ),
        FieldSet(
            "admin_shutdown",
            "is_useg",
            "intra_epg_isolation",
            "preferred_group_member",
            "qos_class",
            name=_("Policy"),
        ),
    )

    class Meta:
        model = ACIEndpointGroup
        fields = (
            "aci_tenant",
            "aci_app_profile",
            "aci_bridge_domain",
            "name",
            "name_alias",
            "description",
            "admin_shutdown",
            "is_useg",
            "intra_epg_isolation",
            "preferred_group_member",
            "qos_class",
            "tags",
        )


class ACIEndpointGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIEndpointGroup
    aci_app_profile = DynamicModelChoiceField(queryset=ACIAppProfile.objects.all(), required=False)
    aci_bridge_domain = DynamicModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(), required=False
    )
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)
    admin_shutdown = forms.NullBooleanField(required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIEndpointGroupFilterForm(NetBoxModelFilterSetForm):
    model = ACIEndpointGroup
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    aci_app_profile_id = DynamicModelMultipleChoiceField(
        queryset=ACIAppProfile.objects.all(), required=False, label=_("App Profile")
    )
    aci_bridge_domain_id = DynamicModelMultipleChoiceField(
        queryset=ACIBridgeDomain.objects.all(), required=False, label=_("Bridge Domain")
    )
    is_useg = forms.NullBooleanField(required=False)


class ACIEndpointGroupImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    aci_app_profile = forms.ModelChoiceField(
        queryset=ACIAppProfile.objects.all(), to_field_name="name"
    )
    aci_bridge_domain = forms.ModelChoiceField(
        queryset=ACIBridgeDomain.objects.all(), to_field_name="name"
    )

    class Meta:
        model = ACIEndpointGroup
        fields = (
            "aci_tenant",
            "aci_app_profile",
            "aci_bridge_domain",
            "name",
            "name_alias",
            "description",
            "admin_shutdown",
            "is_useg",
            "intra_epg_isolation",
            "preferred_group_member",
            "qos_class",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIUSegAttribute
# ---------------------------------------------------------------------------

class ACIUSegAttributeForm(NetBoxModelForm):
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.filter(is_useg=True), label=_("Endpoint Group")
    )

    class Meta:
        model = ACIUSegAttribute
        fields = (
            "aci_endpoint_group",
            "name",
            "name_alias",
            "attribute_type",
            "match_operator",
            "match_value",
            "description",
            "tags",
        )


class ACIUSegAttributeBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIUSegAttribute
    aci_endpoint_group = DynamicModelChoiceField(
        queryset=ACIEndpointGroup.objects.filter(is_useg=True), required=False
    )
    attribute_type = forms.ChoiceField(choices=USegAttributeTypeChoices, required=False)
    match_operator = forms.ChoiceField(choices=USegAttributeMatchOperatorChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias")


class ACIUSegAttributeFilterForm(NetBoxModelFilterSetForm):
    model = ACIUSegAttribute
    aci_endpoint_group_id = DynamicModelMultipleChoiceField(
        queryset=ACIEndpointGroup.objects.filter(is_useg=True),
        required=False,
        label=_("Endpoint Group"),
    )
    attribute_type = forms.MultipleChoiceField(choices=USegAttributeTypeChoices, required=False)


class ACIUSegAttributeImportForm(NetBoxModelImportForm):
    aci_endpoint_group = forms.ModelChoiceField(
        queryset=ACIEndpointGroup.objects.filter(is_useg=True), to_field_name="name"
    )

    class Meta:
        model = ACIUSegAttribute
        fields = (
            "aci_endpoint_group",
            "name",
            "name_alias",
            "attribute_type",
            "match_operator",
            "match_value",
            "description",
            "tags",
        )


# ---------------------------------------------------------------------------
# ACIEndpointSecurityGroup
# ---------------------------------------------------------------------------

class ACIEndpointSecurityGroupForm(NetBoxModelForm):
    aci_tenant = DynamicModelChoiceField(queryset=ACITenant.objects.all(), label=_("Tenant"))
    aci_vrf = DynamicModelChoiceField(
        queryset=ACIVRF.objects.all(),
        label=_("VRF"),
        query_params={"aci_tenant_id": "$aci_tenant"},
    )
    aci_app_profile = DynamicModelChoiceField(
        queryset=ACIAppProfile.objects.all(),
        label=_("App Profile"),
        required=False,
        query_params={"aci_tenant_id": "$aci_tenant"},
    )

    fieldsets = (
        FieldSet(
            "aci_tenant",
            "aci_vrf",
            "aci_app_profile",
            "name",
            "name_alias",
            "description",
            name=_("Endpoint Security Group"),
        ),
        FieldSet(
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "qos_class",
            name=_("Policy"),
        ),
    )

    class Meta:
        model = ACIEndpointSecurityGroup
        fields = (
            "aci_tenant",
            "aci_vrf",
            "aci_app_profile",
            "name",
            "name_alias",
            "description",
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "qos_class",
            "tags",
        )


class ACIEndpointSecurityGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = ACIEndpointSecurityGroup
    aci_vrf = DynamicModelChoiceField(queryset=ACIVRF.objects.all(), required=False)
    qos_class = forms.ChoiceField(choices=QualityOfServiceClassChoices, required=False)
    description = forms.CharField(max_length=128, required=False)
    nullable_fields = ("description", "name_alias", "aci_app_profile")


class ACIEndpointSecurityGroupFilterForm(NetBoxModelFilterSetForm):
    model = ACIEndpointSecurityGroup
    aci_tenant_id = DynamicModelMultipleChoiceField(
        queryset=ACITenant.objects.all(), required=False, label=_("Tenant")
    )
    aci_vrf_id = DynamicModelMultipleChoiceField(
        queryset=ACIVRF.objects.all(), required=False, label=_("VRF")
    )


class ACIEndpointSecurityGroupImportForm(NetBoxModelImportForm):
    aci_tenant = forms.ModelChoiceField(queryset=ACITenant.objects.all(), to_field_name="name")
    aci_vrf = forms.ModelChoiceField(queryset=ACIVRF.objects.all(), to_field_name="name")
    aci_app_profile = forms.ModelChoiceField(
        queryset=ACIAppProfile.objects.all(), to_field_name="name", required=False
    )

    class Meta:
        model = ACIEndpointSecurityGroup
        fields = (
            "aci_tenant",
            "aci_vrf",
            "aci_app_profile",
            "name",
            "name_alias",
            "description",
            "admin_shutdown",
            "preferred_group_member",
            "intra_esg_isolation",
            "qos_class",
            "tags",
        )
