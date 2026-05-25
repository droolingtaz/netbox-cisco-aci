"""Phase 2 — Tenancy.

Adds Tenant, VRF, Bridge Domain (+ Subnet), App Profile, Endpoint Group,
uSeg Attribute, and Endpoint Security Group.
"""

import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


def _aci_base_fields():
    return [
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
        ("created", models.DateTimeField(auto_now_add=True, null=True)),
        ("last_updated", models.DateTimeField(auto_now=True, null=True)),
        (
            "custom_field_data",
            models.JSONField(
                blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder
            ),
        ),
        ("name", models.CharField(max_length=64)),
        ("name_alias", models.CharField(blank=True, max_length=64)),
        ("description", models.CharField(blank=True, max_length=128)),
    ]


def _tags_field():
    return (
        "tags",
        taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0001_initial"),
        ("ipam", "0001_initial"),
        ("netbox_aci", "0001_initial"),
    ]

    operations = [
        # ----- ACITenant -----
        migrations.CreateModel(
            name="ACITenant",
            fields=_aci_base_fields() + [
                (
                    "aci_fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tenants",
                        to="netbox_aci.acifabric",
                    ),
                ),
                _tags_field(),
            ],
            options={"verbose_name": "ACI Tenant", "verbose_name_plural": "ACI Tenants", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="acitenant",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_aci_acitenant_fabric_name_unique",
            ),
        ),

        # ----- ACIVRF -----
        migrations.CreateModel(
            name="ACIVRF",
            fields=_aci_base_fields() + [
                (
                    "aci_tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vrfs",
                        to="netbox_aci.acitenant",
                    ),
                ),
                (
                    "nb_vrf",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="ipam.vrf",
                    ),
                ),
                ("policy_enforcement_preference", models.CharField(default="enforced", max_length=16)),
                ("policy_enforcement_direction", models.CharField(default="ingress", max_length=16)),
                ("bd_enforcement_enabled", models.BooleanField(default=False)),
                ("preferred_group_enabled", models.BooleanField(default=False)),
                _tags_field(),
            ],
            options={"verbose_name": "ACI VRF", "verbose_name_plural": "ACI VRFs", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="acivrf",
            constraint=models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_aci_acivrf_tenant_name_unique",
            ),
        ),

        # ----- ACIBridgeDomain -----
        migrations.CreateModel(
            name="ACIBridgeDomain",
            fields=_aci_base_fields() + [
                (
                    "aci_tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bridge_domains",
                        to="netbox_aci.acitenant",
                    ),
                ),
                (
                    "aci_vrf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="bridge_domains",
                        to="netbox_aci.acivrf",
                    ),
                ),
                ("unicast_routing_enabled", models.BooleanField(default=True)),
                ("arp_flooding_enabled", models.BooleanField(default=False)),
                ("limit_ip_learn_to_subnets", models.BooleanField(default=True)),
                ("l2_unknown_unicast", models.CharField(default="proxy", max_length=16)),
                ("l3_unknown_multicast", models.CharField(default="flood", max_length=16)),
                ("multi_destination_flooding", models.CharField(default="bd-flood", max_length=16)),
                ("mac_address", models.CharField(blank=True, max_length=17)),
                _tags_field(),
            ],
            options={"verbose_name": "ACI Bridge Domain", "verbose_name_plural": "ACI Bridge Domains", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="acibridgedomain",
            constraint=models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_aci_acibd_tenant_name_unique",
            ),
        ),

        # ----- ACIBridgeDomainSubnet -----
        migrations.CreateModel(
            name="ACIBridgeDomainSubnet",
            fields=_aci_base_fields() + [
                (
                    "aci_bridge_domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subnets",
                        to="netbox_aci.acibridgedomain",
                    ),
                ),
                ("gateway_ip", models.CharField(max_length=64)),
                (
                    "nb_prefix",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="ipam.prefix",
                    ),
                ),
                ("scope_public", models.BooleanField(default=False)),
                ("scope_shared", models.BooleanField(default=False)),
                ("scope_private", models.BooleanField(default=True)),
                ("is_primary", models.BooleanField(default=False)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI BD Subnet",
                "verbose_name_plural": "ACI BD Subnets",
                "ordering": ("aci_bridge_domain", "gateway_ip"),
            },
        ),
        migrations.AddConstraint(
            model_name="acibridgedomainsubnet",
            constraint=models.UniqueConstraint(
                fields=("aci_bridge_domain", "gateway_ip"),
                name="netbox_aci_acibdsubnet_bd_gw_unique",
            ),
        ),

        # ----- ACIAppProfile -----
        migrations.CreateModel(
            name="ACIAppProfile",
            fields=_aci_base_fields() + [
                (
                    "aci_tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="app_profiles",
                        to="netbox_aci.acitenant",
                    ),
                ),
                _tags_field(),
            ],
            options={"verbose_name": "ACI Application Profile", "verbose_name_plural": "ACI Application Profiles", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="aciappprofile",
            constraint=models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_aci_aciappprofile_tenant_name_unique",
            ),
        ),

        # ----- ACIEndpointGroup -----
        migrations.CreateModel(
            name="ACIEndpointGroup",
            fields=_aci_base_fields() + [
                (
                    "aci_tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_groups",
                        to="netbox_aci.acitenant",
                    ),
                ),
                (
                    "aci_app_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_groups",
                        to="netbox_aci.aciappprofile",
                    ),
                ),
                (
                    "aci_bridge_domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_groups",
                        to="netbox_aci.acibridgedomain",
                    ),
                ),
                ("admin_shutdown", models.BooleanField(default=False)),
                ("is_useg", models.BooleanField(default=False)),
                ("intra_epg_isolation", models.BooleanField(default=False)),
                ("preferred_group_member", models.BooleanField(default=False)),
                ("qos_class", models.CharField(default="unspecified", max_length=16)),
                _tags_field(),
            ],
            options={"verbose_name": "ACI Endpoint Group", "verbose_name_plural": "ACI Endpoint Groups", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="aciendpointgroup",
            constraint=models.UniqueConstraint(
                fields=("aci_app_profile", "name"),
                name="netbox_aci_aciepg_ap_name_unique",
            ),
        ),

        # ----- ACIUSegAttribute -----
        migrations.CreateModel(
            name="ACIUSegAttribute",
            fields=_aci_base_fields() + [
                (
                    "aci_endpoint_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="useg_attributes",
                        to="netbox_aci.aciendpointgroup",
                    ),
                ),
                ("attribute_type", models.CharField(max_length=16)),
                ("match_operator", models.CharField(default="equals", max_length=16)),
                ("match_value", models.CharField(max_length=255)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI uSeg Attribute",
                "verbose_name_plural": "ACI uSeg Attributes",
                "ordering": ("aci_endpoint_group", "attribute_type", "match_value"),
            },
        ),

        # ----- ACIEndpointSecurityGroup -----
        migrations.CreateModel(
            name="ACIEndpointSecurityGroup",
            fields=_aci_base_fields() + [
                (
                    "aci_tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_security_groups",
                        to="netbox_aci.acitenant",
                    ),
                ),
                (
                    "aci_vrf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_security_groups",
                        to="netbox_aci.acivrf",
                    ),
                ),
                (
                    "aci_app_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="endpoint_security_groups",
                        to="netbox_aci.aciappprofile",
                    ),
                ),
                ("admin_shutdown", models.BooleanField(default=False)),
                ("preferred_group_member", models.BooleanField(default=False)),
                ("intra_esg_isolation", models.BooleanField(default=False)),
                ("qos_class", models.CharField(default="unspecified", max_length=16)),
                _tags_field(),
            ],
            options={"verbose_name": "ACI Endpoint Security Group", "verbose_name_plural": "ACI Endpoint Security Groups", "ordering": ("name",)},
        ),
        migrations.AddConstraint(
            model_name="aciendpointsecuritygroup",
            constraint=models.UniqueConstraint(
                fields=("aci_vrf", "name"),
                name="netbox_aci_aciesg_vrf_name_unique",
            ),
        ),
    ]
