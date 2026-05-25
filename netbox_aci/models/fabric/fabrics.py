"""ACI Fabric — the top-level container."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIFabricBaseModel


class ACIFabric(ACIFabricBaseModel):
    """An ACI fabric.

    ACI Fabric IDs are *not* required to be unique across the
    organisation — a customer may have multiple fabrics with the same
    numeric ID at different sites. We therefore only enforce
    name-uniqueness here. Compare with the legacy plugin, which used to
    enforce ``fabric_id`` uniqueness and had to drop that constraint to
    support multi-fabric deployments.
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
                name="netbox_aci_acifabric_name_unique",
            ),
        )

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:acifabric", args=[self.pk])
