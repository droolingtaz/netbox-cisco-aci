"""ACI LLDP interface policy (``lldpIfPol``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import EnabledDisabledChoices
from ...base import ACIFabricBaseModel


class ACILLDPInterfacePolicy(ACIFabricBaseModel):
    """An LLDP interface policy."""

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="lldp_policies",
        verbose_name=_("ACI Fabric"),
    )
    receive_state = models.CharField(
        verbose_name=_("Receive state"),
        max_length=8,
        default=EnabledDisabledChoices.ENABLED,
        choices=EnabledDisabledChoices,
    )
    transmit_state = models.CharField(
        verbose_name=_("Transmit state"),
        max_length=8,
        default=EnabledDisabledChoices.ENABLED,
        choices=EnabledDisabledChoices,
    )

    clone_fields = ("aci_fabric", "receive_state", "transmit_state", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI LLDP Interface Policy")
        verbose_name_plural = _("ACI LLDP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acilldppol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / LLDP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilldpinterfacepolicy", args=[self.pk])
