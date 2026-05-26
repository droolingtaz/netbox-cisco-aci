"""ACI MCP interface policy (``mcpIfPol``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import EnabledDisabledChoices
from ...base import ACIFabricBaseModel


class ACIMCPInterfacePolicy(ACIFabricBaseModel):
    """A Mis-Cabling Protocol policy."""

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="mcp_policies",
        verbose_name=_("ACI Fabric"),
    )
    admin_state = models.CharField(
        verbose_name=_("Admin state"),
        max_length=8,
        default=EnabledDisabledChoices.ENABLED,
        choices=EnabledDisabledChoices,
    )
    strict_mode = models.BooleanField(
        verbose_name=_("Strict mode"),
        default=False,
    )

    clone_fields = ("aci_fabric", "admin_state", "strict_mode", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI MCP Interface Policy")
        verbose_name_plural = _("ACI MCP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acimcppol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / MCP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acimcpinterfacepolicy", args=[self.pk])
