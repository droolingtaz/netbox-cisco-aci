"""ACI Domains (Physical / L3 / VMM / L2-Ext / FC)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import DomainTypeChoices
from ..base import ACIFabricBaseModel


class ACIDomain(ACIFabricBaseModel):
    """An ACI Domain.

    Combines the five APIC domain classes (``physDomP``, ``l3extDomP``,
    ``vmmDomP``, ``l2extDomP``, ``fcDomP``) into a single NetBox model
    keyed by ``domain_type``. Each Domain consumes at most one VLAN Pool
    (via the implicit ``infraRsVlanNs`` relation); we model that
    directly as an FK rather than as a through model since APIC enforces
    the one-pool cap.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="domains",
        verbose_name=_("ACI Fabric"),
    )
    domain_type = models.CharField(
        verbose_name=_("Type"),
        max_length=16,
        choices=DomainTypeChoices,
        help_text=_("Physical, L3 (l3extDomP), VMM (vmmDomP), L2 External, or Fibre Channel."),
    )
    aci_vlan_pool = models.ForeignKey(
        to="netbox_cisco_aci.ACIVLANPool",
        on_delete=models.PROTECT,
        related_name="domains",
        verbose_name=_("ACI VLAN Pool"),
        blank=True,
        null=True,
        help_text=_(
            "VLAN Pool this domain consumes. Required for Physical, L3, VMM "
            "and L2 External domains; Fibre Channel domains use a VSAN pool "
            "(not yet modelled)."
        ),
    )

    clone_fields = ("aci_fabric", "domain_type", "aci_vlan_pool", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Domain")
        verbose_name_plural = _("ACI Domains")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acidomain_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / {self.get_domain_type_display()}-{self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acidomain", args=[self.pk])

    def get_domain_type_color(self) -> str:
        # Visual hint for table/badge rendering.
        return {
            DomainTypeChoices.PHYSICAL: "blue",
            DomainTypeChoices.L3: "purple",
            DomainTypeChoices.VMM: "cyan",
            DomainTypeChoices.L2: "teal",
            DomainTypeChoices.FC: "orange",
        }.get(self.domain_type, "gray")
