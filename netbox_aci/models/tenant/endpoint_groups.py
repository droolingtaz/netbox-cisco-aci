"""ACI Endpoint Group (``fvAEPg``) and uSeg attributes."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    QualityOfServiceClassChoices,
    USegAttributeMatchOperatorChoices,
    USegAttributeTypeChoices,
)
from ...constants import COMMON_TENANT_NAME
from ..base import ACITenantBaseModel


class ACIEndpointGroup(ACITenantBaseModel):
    """An ACI Endpoint Group.

    An EPG lives inside an Application Profile and is backed by a BD.
    ``is_useg`` flips the EPG into uSeg mode, where membership is
    derived from :class:`ACIUSegAttribute` rules rather than static port
    bindings.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="endpoint_groups",
        verbose_name=_("ACI Tenant"),
    )
    aci_app_profile = models.ForeignKey(
        to="netbox_aci.ACIAppProfile",
        on_delete=models.PROTECT,
        related_name="endpoint_groups",
        verbose_name=_("ACI Application Profile"),
    )
    aci_bridge_domain = models.ForeignKey(
        to="netbox_aci.ACIBridgeDomain",
        on_delete=models.PROTECT,
        related_name="endpoint_groups",
        verbose_name=_("ACI Bridge Domain"),
    )

    admin_shutdown = models.BooleanField(
        verbose_name=_("Admin shutdown"),
        default=False,
        help_text=_("When true, ACI removes the EPG policy from all switches."),
    )
    is_useg = models.BooleanField(
        verbose_name=_("uSeg EPG"),
        default=False,
        help_text=_(
            "When true, membership is governed by uSeg attributes rather than "
            "static port bindings."
        ),
    )
    intra_epg_isolation = models.BooleanField(
        verbose_name=_("Intra-EPG isolation"),
        default=False,
    )
    preferred_group_member = models.BooleanField(
        verbose_name=_("Preferred-group member"),
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
        "aci_app_profile",
        "aci_bridge_domain",
        "qos_class",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Endpoint Group")
        verbose_name_plural = _("ACI Endpoint Groups")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_app_profile", "name"),
                name="netbox_aci_aciepg_ap_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_app_profile} / EPG {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:aciendpointgroup", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric

    def clean(self) -> None:
        super().clean()
        # AP / Tenant agreement.
        if self.aci_app_profile_id and self.aci_tenant_id:
            if self.aci_app_profile.aci_tenant_id != self.aci_tenant_id:
                raise ValidationError(
                    {
                        "aci_app_profile": _(
                            "The Application Profile must belong to the EPG's tenant."
                        )
                    }
                )
        # BD must be in the same tenant or in `common`.
        if self.aci_bridge_domain_id and self.aci_tenant_id:
            bd_tenant_id = self.aci_bridge_domain.aci_tenant_id
            if bd_tenant_id != self.aci_tenant_id:
                bd_tenant_name = getattr(self.aci_bridge_domain.aci_tenant, "name", "")
                if bd_tenant_name != COMMON_TENANT_NAME:
                    raise ValidationError(
                        {
                            "aci_bridge_domain": _(
                                "The BD must live in the same tenant as the EPG, "
                                "or in the `common` tenant."
                            )
                        }
                    )


class ACIUSegAttribute(ACITenantBaseModel):
    """A uSeg attribute on an EPG.

    Only valid when the parent EPG has ``is_useg=True``. A given EPG can
    carry many attributes; ACI evaluates them with the EPG's
    match-policy (any vs. all) which lives on the EPG (modelled as
    ``match_all_attributes`` if/when we extend the EPG with that flag).
    """

    aci_endpoint_group = models.ForeignKey(
        to="netbox_aci.ACIEndpointGroup",
        on_delete=models.CASCADE,
        related_name="useg_attributes",
        verbose_name=_("ACI Endpoint Group"),
    )
    attribute_type = models.CharField(
        verbose_name=_("Type"),
        max_length=16,
        choices=USegAttributeTypeChoices,
    )
    match_operator = models.CharField(
        verbose_name=_("Operator"),
        max_length=16,
        default=USegAttributeMatchOperatorChoices.EQUALS,
        choices=USegAttributeMatchOperatorChoices,
    )
    match_value = models.CharField(
        verbose_name=_("Value"),
        max_length=255,
    )

    clone_fields = ("aci_endpoint_group", "attribute_type", "match_operator")

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI uSeg Attribute")
        verbose_name_plural = _("ACI uSeg Attributes")
        ordering = ("aci_endpoint_group", "attribute_type", "match_value")

    def __str__(self) -> str:
        return f"{self.aci_endpoint_group} / {self.attribute_type}={self.match_value}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:aciusegattribute", args=[self.pk])

    def clean(self) -> None:
        super().clean()
        if self.aci_endpoint_group_id and not self.aci_endpoint_group.is_useg:
            raise ValidationError(
                {
                    "aci_endpoint_group": _(
                        "uSeg attributes can only be attached to EPGs with "
                        "`is_useg=True`."
                    )
                }
            )

    @property
    def aci_tenant(self):
        return self.aci_endpoint_group.aci_tenant

    @property
    def aci_fabric(self):
        return self.aci_endpoint_group.aci_fabric
