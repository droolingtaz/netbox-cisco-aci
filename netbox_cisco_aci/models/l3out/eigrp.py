"""ACI EIGRP Interface Policy (``eigrpIfPol``)."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACITenantBaseModel


class ACIEIGRPInterfacePolicy(ACITenantBaseModel):
    """Reusable per-tenant EIGRP interface policy."""

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="eigrp_interface_policies",
        verbose_name=_("ACI Tenant"),
    )
    hello_interval = models.PositiveSmallIntegerField(
        verbose_name=_("Hello interval"),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    hold_interval = models.PositiveSmallIntegerField(
        verbose_name=_("Hold interval"),
        default=15,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    bandwidth = models.PositiveBigIntegerField(
        verbose_name=_("Bandwidth (kbps)"),
        blank=True,
        null=True,
    )
    delay = models.PositiveBigIntegerField(
        verbose_name=_("Delay (tens of microseconds)"),
        blank=True,
        null=True,
    )
    controls = models.JSONField(
        verbose_name=_("Controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: bfd, nh-self, passive, split-horizon."),
    )

    clone_fields = (
        "aci_tenant",
        "hello_interval",
        "hold_interval",
        "bandwidth",
        "delay",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI EIGRP Interface Policy")
        verbose_name_plural = _("ACI EIGRP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acieigrpinterfacepolicy_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acieigrpinterfacepolicy", args=[self.pk])
