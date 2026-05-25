"""Phase 1 — Fabric topology (Fabric, Pod, Node).

This migration is hand-written so the initial schema is reviewable.
After 1.0 we will switch back to ``makemigrations``-generated migrations
to stay aligned with NetBox conventions.
"""

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ACIFabric",
            fields=[
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
                (
                    "fabric_id",
                    models.PositiveSmallIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(128),
                        ],
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name": "ACI Fabric",
                "verbose_name_plural": "ACI Fabrics",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="acifabric",
            constraint=models.UniqueConstraint(
                fields=("name",), name="netbox_cisco_aci_acifabric_name_unique"
            ),
        ),
        migrations.CreateModel(
            name="ACIPod",
            fields=[
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
                (
                    "pod_id",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(254),
                        ]
                    ),
                ),
                (
                    "aci_fabric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pods",
                        to="netbox_cisco_aci.acifabric",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name": "ACI Pod",
                "verbose_name_plural": "ACI Pods",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="acipod",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "pod_id"),
                name="netbox_cisco_aci_acipod_fabric_podid_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="acipod",
            constraint=models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acipod_fabric_name_unique",
            ),
        ),
        migrations.CreateModel(
            name="ACINode",
            fields=[
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
                (
                    "node_id",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(4000),
                        ]
                    ),
                ),
                ("role", models.CharField(default="leaf", max_length=16)),
                ("node_type", models.CharField(default="physical", max_length=16)),
                ("serial_number", models.CharField(blank=True, max_length=64)),
                ("pod_tep_pool", models.CharField(blank=True, max_length=64)),
                ("firmware_version", models.CharField(blank=True, max_length=64)),
                ("node_object_id", models.PositiveBigIntegerField(blank=True, null=True)),
                (
                    "aci_pod",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="nodes",
                        to="netbox_cisco_aci.acipod",
                    ),
                ),
                (
                    "node_object_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name": "ACI Node",
                "verbose_name_plural": "ACI Nodes",
                "ordering": ("name",),
            },
        ),
        migrations.AddConstraint(
            model_name="acinode",
            constraint=models.UniqueConstraint(
                fields=("aci_pod", "node_id"),
                name="netbox_cisco_aci_acinode_pod_nodeid_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="acinode",
            constraint=models.UniqueConstraint(
                fields=("aci_pod", "name"),
                name="netbox_cisco_aci_acinode_pod_name_unique",
            ),
        ),
    ]
