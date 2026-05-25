"""Phase 3 \u2014 Access policies: VLAN Pools, Domains, AAEPs."""

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
        ("netbox_cisco_aci", "0002_tenancy"),
    ]

    operations = [
        # ----- ACIVLANPool -----
        migrations.CreateModel(
            name="ACIVLANPool",
            fields=_aci_base_fields() + [
                (
                    "aci_fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vlan_pools",
                        to="netbox_cisco_aci.acifabric",
                    ),
                ),
                ("allocation_mode", models.CharField(default="static", max_length=16)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI VLAN Pool",
                "verbose_name_plural": "ACI VLAN Pools",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="acivlanpool",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acivlanpool_fabric_name_unique",
            ),
        ),

        # ----- ACIVLANPoolBlock -----
        migrations.CreateModel(
            name="ACIVLANPoolBlock",
            fields=_aci_base_fields() + [
                (
                    "aci_vlan_pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocks",
                        to="netbox_cisco_aci.acivlanpool",
                    ),
                ),
                ("from_vlan", models.PositiveSmallIntegerField()),
                ("to_vlan", models.PositiveSmallIntegerField()),
                ("allocation_mode_override", models.CharField(blank=True, max_length=16)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI VLAN Pool Block",
                "verbose_name_plural": "ACI VLAN Pool Blocks",
                "ordering": ("aci_vlan_pool", "from_vlan", "to_vlan"),
            },
        ),
        migrations.AddConstraint(
            model_name="acivlanpoolblock",
            constraint=models.UniqueConstraint(
                fields=("aci_vlan_pool", "from_vlan", "to_vlan"),
                name="netbox_cisco_aci_acivlanpoolblock_pool_range_unique",
            ),
        ),

        # ----- ACIDomain -----
        migrations.CreateModel(
            name="ACIDomain",
            fields=_aci_base_fields() + [
                (
                    "aci_fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="domains",
                        to="netbox_cisco_aci.acifabric",
                    ),
                ),
                ("domain_type", models.CharField(max_length=16)),
                (
                    "aci_vlan_pool",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="domains",
                        to="netbox_cisco_aci.acivlanpool",
                    ),
                ),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI Domain",
                "verbose_name_plural": "ACI Domains",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="acidomain",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acidomain_fabric_name_unique",
            ),
        ),

        # ----- ACIAAEP -----
        migrations.CreateModel(
            name="ACIAAEP",
            fields=_aci_base_fields() + [
                (
                    "aci_fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="aaeps",
                        to="netbox_cisco_aci.acifabric",
                    ),
                ),
                ("enable_infra_vlan", models.BooleanField(default=False)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI AAEP",
                "verbose_name_plural": "ACI AAEPs",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="aciaaep",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_aciaaep_fabric_name_unique",
            ),
        ),

        # ----- ACIAAEPDomainAssociation (through) -----
        migrations.CreateModel(
            name="ACIAAEPDomainAssociation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "aci_aaep",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domain_associations",
                        to="netbox_cisco_aci.aciaaep",
                    ),
                ),
                (
                    "aci_domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="aaep_associations",
                        to="netbox_cisco_aci.acidomain",
                    ),
                ),
            ],
            options={
                "verbose_name": "ACI AAEP-Domain Association",
                "verbose_name_plural": "ACI AAEP-Domain Associations",
                "ordering": ("aci_aaep", "aci_domain"),
            },
        ),
        migrations.AddConstraint(
            model_name="aciaaepdomainassociation",
            constraint=models.UniqueConstraint(
                fields=("aci_aaep", "aci_domain"),
                name="netbox_cisco_aci_aciaaepdomain_unique",
            ),
        ),
        # Wire the M2M through table.
        migrations.AddField(
            model_name="aciaaep",
            name="domains",
            field=models.ManyToManyField(
                related_name="aaeps",
                through="netbox_cisco_aci.ACIAAEPDomainAssociation",
                to="netbox_cisco_aci.acidomain",
            ),
        ),

        # ----- ACIAAEPEPGMapping -----
        migrations.CreateModel(
            name="ACIAAEPEPGMapping",
            fields=_aci_base_fields() + [
                (
                    "aci_aaep",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="epg_mappings",
                        to="netbox_cisco_aci.aciaaep",
                    ),
                ),
                (
                    "aci_endpoint_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="aaep_mappings",
                        to="netbox_cisco_aci.aciendpointgroup",
                    ),
                ),
                ("encap_vlan", models.PositiveSmallIntegerField()),
                ("mode", models.CharField(default="regular", max_length=16)),
                _tags_field(),
            ],
            options={
                "verbose_name": "ACI AAEP-EPG Mapping",
                "verbose_name_plural": "ACI AAEP-EPG Mappings",
                "ordering": ("aci_aaep", "encap_vlan"),
            },
        ),
        migrations.AddConstraint(
            model_name="aciaaepepgmapping",
            constraint=models.UniqueConstraint(
                fields=("aci_aaep", "aci_endpoint_group", "encap_vlan"),
                name="netbox_cisco_aci_aciaaepepgmap_unique",
            ),
        ),
    ]
