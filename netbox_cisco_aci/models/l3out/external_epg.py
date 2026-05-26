"""ACI External EPG + External EPG Subnet (``l3extInstP`` / ``l3extSubnet``)."""

import ipaddress

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import QualityOfServiceClassChoices
from ..base import ACIBaseModel


class ACIExternalEPG(ACIBaseModel):
    """Identity for contract attachment on an L3Out (``l3extInstP``)."""

    aci_l3out = models.ForeignKey(
        to="netbox_cisco_aci.ACIL3Out",
        on_delete=models.CASCADE,
        related_name="external_epgs",
        verbose_name=_("ACI L3Out"),
    )
    qos_class = models.CharField(
        verbose_name=_("QoS class"),
        max_length=16,
        blank=True,
        choices=QualityOfServiceClassChoices,
    )
    target_dscp = models.CharField(
        verbose_name=_("Target DSCP"),
        max_length=32,
        blank=True,
    )
    preferred_group_member = models.BooleanField(
        verbose_name=_("Preferred group member"),
        default=False,
    )

    clone_fields = (
        "aci_l3out",
        "qos_class",
        "target_dscp",
        "preferred_group_member",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI External EPG")
        verbose_name_plural = _("ACI External EPGs")
        ordering = ("aci_l3out", "name")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_l3out", "name"),
                name="netbox_cisco_aci_aciexternalepg_l3out_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_l3out} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciexternalepg", args=[self.pk])

    @property
    def aci_tenant(self):
        return self.aci_l3out.aci_tenant


class ACIExternalEPGSubnet(ACIBaseModel):
    """Prefix scope attached to an External EPG (``l3extSubnet``)."""

    aci_external_epg = models.ForeignKey(
        to="netbox_cisco_aci.ACIExternalEPG",
        on_delete=models.CASCADE,
        related_name="subnets",
        verbose_name=_("External EPG"),
    )
    prefix = models.CharField(
        verbose_name=_("Prefix"),
        max_length=43,
        help_text=_("IPv4 or IPv6 prefix (e.g. 0.0.0.0/0)."),
    )
    scope_controls = models.JSONField(
        verbose_name=_("Scope controls"),
        default=list,
        blank=True,
        help_text=_(
            "Tokens: import-rtctrl, export-rtctrl, shared-rtctrl, import-security, "
            "shared-security, aggregate-import, aggregate-export, aggregate-shared."
        ),
    )

    clone_fields = ("aci_external_epg", "scope_controls", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI External EPG Subnet")
        verbose_name_plural = _("ACI External EPG Subnets")
        ordering = ("aci_external_epg", "prefix")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_external_epg", "prefix"),
                name="netbox_cisco_aci_aciexternalepgsubnet_extepg_prefix_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_external_epg} / {self.prefix}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciexternalepgsubnet", args=[self.pk])

    def clean(self) -> None:
        super().clean()

        if self.prefix:
            try:
                ipaddress.ip_network(self.prefix, strict=False)
            except ValueError as exc:
                raise ValidationError(
                    {"prefix": _("Invalid prefix: %(err)s") % {"err": str(exc)}}
                ) from exc

        if self.scope_controls and not isinstance(self.scope_controls, list):
            raise ValidationError({"scope_controls": _("Must be a JSON list of strings.")})
