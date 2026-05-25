"""ACI Tenant — the top-level policy container inside a Fabric."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIFabricBaseModel


class ACITenant(ACIFabricBaseModel):
    """An ACI Tenant.

    Tenants live inside a Fabric. The well-known names ``common``,
    ``infra``, and ``mgmt`` are reserved per Cisco's conventions and are
    flagged read-only-ish by the form layer, but the model itself does
    not refuse them — a fresh fabric needs ``common`` to exist.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="tenants",
        verbose_name=_("ACI Fabric"),
    )

    clone_fields = ("aci_fabric", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Tenant")
        verbose_name_plural = _("ACI Tenants")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_aci_acitenant_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:acitenant", args=[self.pk])
