"""ACI Interface Policy Groups (``infraAccPortGrp`` / ``infraAccBndlGrp``).

A Policy Group bundles every per-policy ref (Link Level, CDP, LLDP,
LACP, MCP, STP) plus an AAEP and pins them onto a set of physical
ports. The ``pg_type`` discriminator picks between an access port group,
a port-channel bundle, or a virtual-PC bundle.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import InterfacePolicyGroupTypeChoices
from ..base import ACIFabricBaseModel


class ACIInterfacePolicyGroup(ACIFabricBaseModel):
    """An Interface Policy Group."""

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="interface_policy_groups",
        verbose_name=_("ACI Fabric"),
    )
    pg_type = models.CharField(
        verbose_name=_("Type"),
        max_length=8,
        choices=InterfacePolicyGroupTypeChoices,
        db_index=True,
    )
    link_level_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACILinkLevelPolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("Link Level policy"),
        blank=True,
        null=True,
    )
    cdp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACICDPInterfacePolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("CDP policy"),
        blank=True,
        null=True,
    )
    lldp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACILLDPInterfacePolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("LLDP policy"),
        blank=True,
        null=True,
    )
    lacp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACILACPInterfacePolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("LACP policy"),
        blank=True,
        null=True,
    )
    mcp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIMCPInterfacePolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("MCP policy"),
        blank=True,
        null=True,
    )
    stp_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACISTPInterfacePolicy",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("STP policy"),
        blank=True,
        null=True,
    )
    aaep = models.ForeignKey(
        to="netbox_cisco_aci.ACIAAEP",
        on_delete=models.SET_NULL,
        related_name="policy_groups",
        verbose_name=_("AAEP"),
        blank=True,
        null=True,
    )

    clone_fields = ("aci_fabric", "pg_type", "aaep", "description")

    _POLICY_FK_FIELDS = (
        "link_level_policy",
        "cdp_policy",
        "lldp_policy",
        "lacp_policy",
        "mcp_policy",
        "stp_policy",
        "aaep",
    )

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Interface Policy Group")
        verbose_name_plural = _("ACI Interface Policy Groups")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_aciintfpg_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / {self.get_pg_type_display()} {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciinterfacepolicygroup", args=[self.pk])

    def get_pg_type_color(self) -> str:
        return {
            InterfacePolicyGroupTypeChoices.ACCESS: "gray",
            InterfacePolicyGroupTypeChoices.PC: "blue",
            InterfacePolicyGroupTypeChoices.VPC: "purple",
        }.get(self.pg_type, "gray")

    def clean(self) -> None:
        super().clean()
        # LACP is required for port-channel / vPC bundles.
        if (
            self.pg_type
            in (
                InterfacePolicyGroupTypeChoices.PC,
                InterfacePolicyGroupTypeChoices.VPC,
            )
            and not self.lacp_policy_id
        ):
            raise ValidationError(
                {"lacp_policy": _("A LACP policy is required for PC/vPC policy groups.")}
            )
        # Cross-fabric guard for every policy FK + AAEP.
        if not self.aci_fabric_id:
            return
        for field in self._POLICY_FK_FIELDS:
            ref = getattr(self, field, None)
            if ref is None:
                continue
            if ref.aci_fabric_id != self.aci_fabric_id:
                raise ValidationError(
                    {
                        field: _("%(ref)s belongs to a different Fabric than this Policy Group.")
                        % {"ref": ref.name}
                    }
                )
