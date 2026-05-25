"""ACI VRF (Context) — L3 isolation domain inside a Tenant."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    VRFPolicyEnforcementChoices,
    VRFPolicyEnforcementPreferenceChoices,
)
from ..base import ACITenantBaseModel


class ACIVRF(ACITenantBaseModel):
    """An ACI VRF (a.k.a. Context, ``fvCtx``).

    Optionally links to a ``ipam.VRF`` so existing NetBox VRF records can
    serve as the source of truth for routed-IP scoping.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="vrfs",
        verbose_name=_("ACI Tenant"),
    )
    nb_vrf = models.ForeignKey(
        to="ipam.VRF",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("NetBox VRF"),
        help_text=_(
            "Optional link to a NetBox ipam.VRF. Useful when the same VRF is "
            "already documented for routed-IP / IPAM purposes."
        ),
    )
    policy_enforcement_preference = models.CharField(
        verbose_name=_("Policy enforcement preference"),
        max_length=16,
        default=VRFPolicyEnforcementPreferenceChoices.ENFORCED,
        choices=VRFPolicyEnforcementPreferenceChoices,
    )
    policy_enforcement_direction = models.CharField(
        verbose_name=_("Policy enforcement direction"),
        max_length=16,
        default=VRFPolicyEnforcementChoices.INGRESS,
        choices=VRFPolicyEnforcementChoices,
    )
    bd_enforcement_enabled = models.BooleanField(
        verbose_name=_("BD enforcement"),
        default=False,
        help_text=_("Restricts BD-to-BD traffic within the VRF."),
    )
    preferred_group_enabled = models.BooleanField(
        verbose_name=_("Preferred group"),
        default=False,
        help_text=_(
            "When enabled, EPGs marked as preferred-group members exchange "
            "traffic freely without contracts."
        ),
    )

    clone_fields = (
        "aci_tenant",
        "policy_enforcement_preference",
        "policy_enforcement_direction",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI VRF")
        verbose_name_plural = _("ACI VRFs")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acivrf_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acivrf", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric
