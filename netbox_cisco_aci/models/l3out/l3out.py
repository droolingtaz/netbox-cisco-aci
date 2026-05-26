"""ACI L3Out (``l3extOut``)."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...constants import COMMON_TENANT_NAME
from ..base import ACITenantBaseModel


class ACIL3Out(ACITenantBaseModel):
    """Layer-3 out connection from a fabric VRF to the outside world.

    A single L3Out is anchored in one VRF (in this tenant or in the
    ``common`` tenant) and enables one or more routing protocols
    (BGP / OSPF / EIGRP / Static). At least one protocol must be enabled.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="l3outs",
        verbose_name=_("ACI Tenant"),
    )
    aci_vrf = models.ForeignKey(
        to="netbox_cisco_aci.ACIVRF",
        on_delete=models.PROTECT,
        related_name="l3outs",
        verbose_name=_("ACI VRF"),
        help_text=_("VRF anchoring this L3Out. May live in the same tenant or in common."),
    )
    protocol_bgp = models.BooleanField(verbose_name=_("BGP"), default=False)
    protocol_ospf = models.BooleanField(verbose_name=_("OSPF"), default=False)
    protocol_eigrp = models.BooleanField(verbose_name=_("EIGRP"), default=False)
    protocol_static = models.BooleanField(verbose_name=_("Static"), default=True)
    target_dscp = models.CharField(
        verbose_name=_("Target DSCP"),
        max_length=32,
        blank=True,
    )

    clone_fields = (
        "aci_tenant",
        "aci_vrf",
        "protocol_bgp",
        "protocol_ospf",
        "protocol_eigrp",
        "protocol_static",
        "target_dscp",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI L3Out")
        verbose_name_plural = _("ACI L3Outs")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acil3out_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acil3out", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric

    def clean(self) -> None:
        super().clean()

        # VRF must live in the same tenant or in the `common` tenant.
        if self.aci_vrf_id and self.aci_tenant_id:
            vrf_tenant_id = getattr(self.aci_vrf, "aci_tenant_id", None)
            if vrf_tenant_id and vrf_tenant_id != self.aci_tenant_id:
                vrf_tenant_name = getattr(self.aci_vrf.aci_tenant, "name", "")
                if vrf_tenant_name != COMMON_TENANT_NAME:
                    raise ValidationError(
                        {
                            "aci_vrf": _(
                                "The VRF must belong to the same tenant as the L3Out, "
                                "or to the `common` tenant."
                            )
                        }
                    )

        # At least one routing protocol must be enabled.
        if not (
            self.protocol_bgp or self.protocol_ospf or self.protocol_eigrp or self.protocol_static
        ):
            raise ValidationError(
                _("At least one routing protocol (BGP / OSPF / EIGRP / Static) must be enabled.")
            )
