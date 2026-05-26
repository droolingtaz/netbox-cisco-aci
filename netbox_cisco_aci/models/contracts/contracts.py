"""ACI Contract (``vzBrCP``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import ContractScopeChoices, QualityOfServiceClassChoices
from ..base import ACITenantBaseModel


class ACIContract(ACITenantBaseModel):
    """A reusable security policy between EPGs/ESGs."""

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="contracts",
        verbose_name=_("ACI Tenant"),
    )
    scope = models.CharField(
        verbose_name=_("Scope"),
        max_length=32,
        default=ContractScopeChoices.SCOPE_VRF,
        choices=ContractScopeChoices,
        help_text=_("Enforcement scope (VRF/context, tenant, app-profile, or global)."),
    )
    qos_class = models.CharField(
        verbose_name=_("QoS class"),
        max_length=16,
        blank=True,
        choices=QualityOfServiceClassChoices,
        help_text=_("QoS class applied to traffic matched by this contract."),
    )
    target_dscp = models.CharField(
        verbose_name=_("Target DSCP"),
        max_length=32,
        blank=True,
        help_text=_("APIC accepts named DSCP values such as ``CS0`` or ``EF``."),
    )

    clone_fields = ("aci_tenant", "scope", "qos_class", "target_dscp", "description")

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Contract")
        verbose_name_plural = _("ACI Contracts")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acicontract_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acicontract", args=[self.pk])
