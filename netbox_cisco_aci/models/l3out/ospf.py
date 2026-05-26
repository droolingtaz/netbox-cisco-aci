"""ACI OSPF Interface Policy + Attachment."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import OSPFAreaTypeChoices, OSPFNetworkTypeChoices
from ...constants import COMMON_TENANT_NAME
from ..base import ACIBaseModel, ACITenantBaseModel


class ACIOSPFInterfacePolicy(ACITenantBaseModel):
    """Reusable per-tenant OSPF interface policy (``ospfIfPol``)."""

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="ospf_interface_policies",
        verbose_name=_("ACI Tenant"),
    )
    network_type = models.CharField(
        verbose_name=_("Network type"),
        max_length=16,
        default=OSPFNetworkTypeChoices.UNSPECIFIED,
        choices=OSPFNetworkTypeChoices,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_("Priority"),
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(255)],
    )
    cost = models.PositiveSmallIntegerField(
        verbose_name=_("Cost"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(65535)],
    )
    hello_interval = models.PositiveSmallIntegerField(
        verbose_name=_("Hello interval"),
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    dead_interval = models.PositiveSmallIntegerField(
        verbose_name=_("Dead interval"),
        default=40,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    retransmit_interval = models.PositiveSmallIntegerField(
        verbose_name=_("Retransmit interval"),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    transmit_delay = models.PositiveSmallIntegerField(
        verbose_name=_("Transmit delay"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(450)],
    )
    controls = models.JSONField(
        verbose_name=_("Controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: advert-subnet, bfd, mtu-ignore, passive."),
    )

    clone_fields = (
        "aci_tenant",
        "network_type",
        "priority",
        "cost",
        "hello_interval",
        "dead_interval",
        "retransmit_interval",
        "transmit_delay",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI OSPF Interface Policy")
        verbose_name_plural = _("ACI OSPF Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_aciospfinterfacepolicy_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciospfinterfacepolicy", args=[self.pk])


_OSPF_AREA_DOTTED = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def _validate_ospf_area_id(value: str) -> None:
    """Accept either a non-negative 32-bit int as decimal or dotted-quad."""
    if not value:
        raise ValidationError(_("OSPF area ID is required."))
    if _OSPF_AREA_DOTTED.match(value):
        for octet in value.split("."):
            if not 0 <= int(octet) <= 255:
                raise ValidationError(_("Invalid OSPF area ID %(v)s.") % {"v": value})
        return
    try:
        n = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(_("Invalid OSPF area ID %(v)s.") % {"v": value}) from exc
    if not 0 <= n <= 0xFFFFFFFF:
        raise ValidationError(_("OSPF area ID out of range."))


class ACIOSPFInterfaceAttachment(ACIBaseModel):
    """OSPF Interface Policy attached to a Logical Interface Profile."""

    aci_logical_interface_profile = models.OneToOneField(
        to="netbox_cisco_aci.ACILogicalInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="ospf_attachment",
        verbose_name=_("Logical Interface Profile"),
    )
    aci_ospf_interface_policy = models.ForeignKey(
        to="netbox_cisco_aci.ACIOSPFInterfacePolicy",
        on_delete=models.PROTECT,
        related_name="attachments",
        verbose_name=_("OSPF Interface Policy"),
    )
    ospf_area_id = models.CharField(
        verbose_name=_("OSPF area ID"),
        max_length=15,
        help_text=_("Decimal integer or dotted-quad (e.g. 0.0.0.0)."),
    )
    ospf_area_type = models.CharField(
        verbose_name=_("OSPF area type"),
        max_length=16,
        default=OSPFAreaTypeChoices.REGULAR,
        choices=OSPFAreaTypeChoices,
    )
    ospf_area_cost = models.PositiveIntegerField(
        verbose_name=_("OSPF area cost"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(16777215)],
    )

    clone_fields = (
        "aci_ospf_interface_policy",
        "ospf_area_id",
        "ospf_area_type",
        "ospf_area_cost",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI OSPF Interface Attachment")
        verbose_name_plural = _("ACI OSPF Interface Attachments")
        ordering = ("aci_logical_interface_profile",)

    def __str__(self) -> str:
        lip = self.aci_logical_interface_profile
        return f"{lip} OSPF area {self.ospf_area_id}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciospfinterfaceattachment", args=[self.pk])

    def clean(self) -> None:
        super().clean()

        if self.ospf_area_id:
            _validate_ospf_area_id(self.ospf_area_id)

        # Cross-tenant guard: policy tenant must match L3Out tenant or be `common`.
        if self.aci_ospf_interface_policy_id and self.aci_logical_interface_profile_id:
            policy_tenant_id = getattr(self.aci_ospf_interface_policy, "aci_tenant_id", None)
            lip = self.aci_logical_interface_profile
            l3out_tenant_id = getattr(
                getattr(getattr(lip, "aci_logical_node_profile", None), "aci_l3out", None),
                "aci_tenant_id",
                None,
            )
            if policy_tenant_id and l3out_tenant_id and policy_tenant_id != l3out_tenant_id:
                policy_tenant_name = getattr(self.aci_ospf_interface_policy.aci_tenant, "name", "")
                if policy_tenant_name != COMMON_TENANT_NAME:
                    raise ValidationError(
                        {
                            "aci_ospf_interface_policy": _(
                                "The OSPF Interface Policy must belong to the same tenant "
                                "as the L3Out, or to the `common` tenant."
                            )
                        }
                    )
