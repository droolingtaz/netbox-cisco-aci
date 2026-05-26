"""ACI CDP interface policy (``cdpIfPol``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import EnabledDisabledChoices
from ...base import ACIFabricBaseModel


class ACICDPInterfacePolicy(ACIFabricBaseModel):
    """A CDP interface policy.

    APIC ships with ``admin_state`` defaulting to ``disabled`` to match
    Cisco's hardening posture; flip to ``enabled`` per port group as
    needed.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="cdp_policies",
        verbose_name=_("ACI Fabric"),
    )
    admin_state = models.CharField(
        verbose_name=_("Admin state"),
        max_length=8,
        default=EnabledDisabledChoices.DISABLED,
        choices=EnabledDisabledChoices,
    )

    clone_fields = ("aci_fabric", "admin_state", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI CDP Interface Policy")
        verbose_name_plural = _("ACI CDP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acicdppol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / CDP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acicdpinterfacepolicy", args=[self.pk])
