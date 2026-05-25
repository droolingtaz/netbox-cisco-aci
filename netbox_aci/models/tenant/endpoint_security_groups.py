"""ACI Endpoint Security Group (``fvESg``)."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import QualityOfServiceClassChoices
from ..base import ACITenantBaseModel


class ACIEndpointSecurityGroup(ACITenantBaseModel):
    """An ACI Endpoint Security Group.

    ESGs are VRF-scoped (not BD-scoped like EPGs), so the FK is to the
    VRF and the AP is optional. The same uniqueness rule (name unique
    inside its container) applies, but the container is the VRF.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="endpoint_security_groups",
        verbose_name=_("ACI Tenant"),
    )
    aci_vrf = models.ForeignKey(
        to="netbox_aci.ACIVRF",
        on_delete=models.PROTECT,
        related_name="endpoint_security_groups",
        verbose_name=_("ACI VRF"),
    )
    aci_app_profile = models.ForeignKey(
        to="netbox_aci.ACIAppProfile",
        on_delete=models.PROTECT,
        related_name="endpoint_security_groups",
        verbose_name=_("ACI Application Profile"),
        blank=True,
        null=True,
        help_text=_(
            "Optional. ESGs do not require an AP, but some operators model "
            "them under one for UI consistency."
        ),
    )

    admin_shutdown = models.BooleanField(
        verbose_name=_("Admin shutdown"),
        default=False,
    )
    preferred_group_member = models.BooleanField(
        verbose_name=_("Preferred-group member"),
        default=False,
    )
    intra_esg_isolation = models.BooleanField(
        verbose_name=_("Intra-ESG isolation"),
        default=False,
    )
    qos_class = models.CharField(
        verbose_name=_("QoS class"),
        max_length=16,
        default=QualityOfServiceClassChoices.UNSPECIFIED,
        choices=QualityOfServiceClassChoices,
    )

    clone_fields = (
        "aci_tenant",
        "aci_vrf",
        "aci_app_profile",
        "qos_class",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Endpoint Security Group")
        verbose_name_plural = _("ACI Endpoint Security Groups")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_vrf", "name"),
                name="netbox_aci_aciesg_vrf_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_vrf} / ESG {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:aciendpointsecuritygroup", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric

    def clean(self) -> None:
        super().clean()
        # VRF must belong to the ESG's tenant.
        if self.aci_vrf_id and self.aci_tenant_id:
            if self.aci_vrf.aci_tenant_id != self.aci_tenant_id:
                raise ValidationError({"aci_vrf": _("The VRF must belong to the ESG's tenant.")})
        if self.aci_app_profile_id and self.aci_tenant_id:
            if self.aci_app_profile.aci_tenant_id != self.aci_tenant_id:
                raise ValidationError(
                    {
                        "aci_app_profile": _(
                            "The Application Profile must belong to the ESG's tenant."
                        )
                    }
                )
