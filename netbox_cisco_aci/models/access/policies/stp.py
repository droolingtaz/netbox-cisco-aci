"""ACI STP interface policy (``stpIfPol``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...base import ACIFabricBaseModel


class ACISTPInterfacePolicy(ACIFabricBaseModel):
    """A Spanning-Tree interface policy.

    Only models the two BPDU guard / filter flags; we'll grow this to
    cover root-guard, loop-guard, etc. as the project demands it.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="stp_policies",
        verbose_name=_("ACI Fabric"),
    )
    bpdu_filter = models.BooleanField(
        verbose_name=_("BPDU filter"),
        default=False,
    )
    bpdu_guard = models.BooleanField(
        verbose_name=_("BPDU guard"),
        default=False,
    )

    clone_fields = ("aci_fabric", "bpdu_filter", "bpdu_guard", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI STP Interface Policy")
        verbose_name_plural = _("ACI STP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acistppol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / STP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acistpinterfacepolicy", args=[self.pk])
