"""Catch up migration state with model state for Phases 1–3.

The hand-written 0001/0002/0003 migrations omitted a handful of
field-level details that the models *do* declare:

* The shared ``aci_policy_name_validator`` on every ``name`` field
  (every concrete model inherits ``name`` from ``ACIBaseModel`` which
  declares the validator).
* ``MinValueValidator(1)`` / ``MaxValueValidator(4094)`` on the VLAN-ID
  fields (``ACIVLANPoolBlock.from_vlan`` / ``to_vlan`` and
  ``ACIAAEPEPGMapping.encap_vlan``).
* ``limit_choices_to`` on ``ACINode.node_object_type`` (the GFK is
  restricted to ``dcim.device`` and ``virtualization.virtualmachine``).
* The ``ACIAAEP.domains`` M2M (declared on the model, missing from the
  Phase-3 migration).

CI happened to pass because none of these need a DDL change — they are
all validation-only / state-only differences. The user-visible symptom
is ``manage.py migrate`` printing:

    Your models in app(s): 'netbox_cisco_aci' have changes that are not
    yet reflected in a migration, and so won't be applied.

This migration is purely state-resyncing: every ``AlterField`` reissues
the field definition exactly as the model declares it, with no schema
impact. ``ACIAAEP.domains`` is brought in as a state-only ``AddField``
(the M2M through-table was already created by Phase 3).
"""

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import netbox_cisco_aci.validators


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("netbox_cisco_aci", "0003_access_policies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aciaaep",
            name="domains",
            field=models.ManyToManyField(
                blank=True,
                related_name="aaeps",
                through="netbox_cisco_aci.ACIAAEPDomainAssociation",
                to="netbox_cisco_aci.acidomain",
            ),
        ),
        migrations.AlterField(
            model_name="aciaaep",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="aciaaepepgmapping",
            name="encap_vlan",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(4094),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="aciaaepepgmapping",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="aciappprofile",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acibridgedomain",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acibridgedomainsubnet",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acidomain",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="aciendpointgroup",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="aciendpointsecuritygroup",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acifabric",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acinode",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acinode",
            name="node_object_type",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(
                    models.Q(("app_label", "dcim"), ("model", "device")),
                    models.Q(("app_label", "virtualization"), ("model", "virtualmachine")),
                    _connector="OR",
                ),
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="acipod",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acitenant",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="aciusegattribute",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acivlanpool",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acivlanpoolblock",
            name="from_vlan",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(4094),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="acivlanpoolblock",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
        migrations.AlterField(
            model_name="acivlanpoolblock",
            name="to_vlan",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(4094),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="acivrf",
            name="name",
            field=models.CharField(
                max_length=64,
                validators=[netbox_cisco_aci.validators.aci_policy_name_validator],
            ),
        ),
    ]
