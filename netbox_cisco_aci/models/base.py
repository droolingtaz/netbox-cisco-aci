"""Abstract base classes shared by every concrete model in the plugin.

Putting common fields here gives us a single place to evolve the
plugin-wide schema (e.g. add a `apic_dn` cache column later) without
touching dozens of model files.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel

from ..constants import ACI_ALIAS_MAX_LEN, ACI_DESCRIPTION_MAX_LEN, ACI_NAME_MAX_LEN
from ..validators import aci_policy_name_validator


class ACIBaseModel(NetBoxModel):
    """Common ACI fields: name, alias, description.

    Every concrete model inherits from one of the ``ACIBaseModel``
    subclasses (``ACIFabricBaseModel`` for fabric-scoped objects,
    ``ACITenantBaseModel`` for tenant-scoped ones). Subclassing directly
    from ``ACIBaseModel`` is reserved for objects that belong to neither
    scope (e.g. plugin-level metadata).
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=ACI_NAME_MAX_LEN,
        validators=[aci_policy_name_validator],
        help_text=_("APIC object name. Letters, digits, dot, dash, underscore, and colon."),
    )
    name_alias = models.CharField(
        verbose_name=_("Alias"),
        max_length=ACI_ALIAS_MAX_LEN,
        blank=True,
        help_text=_("Optional human-friendly alias."),
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=ACI_DESCRIPTION_MAX_LEN,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class ACIFabricBaseModel(ACIBaseModel):
    """Base for objects that live at the fabric scope (Pod, Node, ...)."""

    class Meta(ACIBaseModel.Meta):
        abstract = True


class ACITenantBaseModel(ACIBaseModel):
    """Base for objects that live inside an ACI Tenant."""

    class Meta(ACIBaseModel.Meta):
        abstract = True
