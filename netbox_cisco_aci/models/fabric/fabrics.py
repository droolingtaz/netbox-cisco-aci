"""ACI Fabric — the top-level container."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIFabricBaseModel


class ACIFabric(ACIFabricBaseModel):
    """An ACI fabric.

    **Multi-fabric is a first-class scenario.** A single NetBox
    instance may model any number of independent ACI fabrics side by
    side — e.g. ``DC1`` and ``DC2`` for the same business unit, or one
    production and one staging fabric. The only uniqueness constraint
    on this model is on ``name``; every downstream object (Pod, Node,
    Tenant, VRF, BD, App Profile, EPG, ESG) scopes its uniqueness to
    its parent Fabric (directly or transitively), so two fabrics may
    contain identical objects without colliding.

    **Fabric IDs are explicitly allowed to overlap.** Cisco does not
    require the numeric ``fabric_id`` to be globally unique — customers
    routinely run multiple fabrics that share an ID (typically 1, the
    APIC default). No constraint involves ``fabric_id``; the legacy
    upstream plugin had to drop one when this came up in production,
    and we never added it. The Best-Practice audit may warn on
    duplicates in the future, but the model never refuses them.
    """

    fabric_id = models.PositiveSmallIntegerField(
        verbose_name=_("Fabric ID"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(128)],
        help_text=_(
            "Numeric Fabric ID as configured on the APIC. Defaults to 1 — the "
            "value Cisco ships out of the box."
        ),
    )

    clone_fields = ("description",)

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Fabric")
        verbose_name_plural = _("ACI Fabrics")
        constraints = (
            models.UniqueConstraint(
                fields=("name",),
                name="netbox_cisco_aci_acifabric_name_unique",
            ),
        )

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acifabric", args=[self.pk])
