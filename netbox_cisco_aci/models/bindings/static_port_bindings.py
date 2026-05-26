"""ACI Static Port Binding (``fvRsPathAtt``).

Binds a single ACI Endpoint Group onto a physical NetBox interface on a
leaf with an explicit encap VLAN. This is the canonical "EPG on port"
object in APIC.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    DeploymentImmediacyChoices,
    StaticPortBindingTypeChoices,
    StaticPortModeChoices,
)
from ...constants import VLAN_ID_MAX, VLAN_ID_MIN
from ..base import ACIBaseModel


class ACIStaticPortBinding(ACIBaseModel):
    """EPG ↔ ``dcim.Interface`` binding with encap VLAN."""

    aci_endpoint_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIEndpointGroup",
        on_delete=models.PROTECT,
        related_name="static_port_bindings",
        verbose_name=_("ACI Endpoint Group"),
    )
    dcim_interface = models.ForeignKey(
        to="dcim.Interface",
        on_delete=models.PROTECT,
        related_name="aci_static_port_bindings",
        verbose_name=_("NetBox Interface"),
    )
    binding_type = models.CharField(
        verbose_name=_("Binding type"),
        max_length=32,
        default=StaticPortBindingTypeChoices.REGULAR,
        choices=StaticPortBindingTypeChoices,
    )
    encap_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("Encap VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
    )
    mode = models.CharField(
        verbose_name=_("Mode"),
        max_length=16,
        default=StaticPortModeChoices.TRUNK,
        choices=StaticPortModeChoices,
    )
    primary_encap_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("Primary encap VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
        blank=True,
        null=True,
        help_text=_("Only meaningful when the EPG is a uSeg EPG."),
    )
    deployment_immediacy = models.CharField(
        verbose_name=_("Deployment immediacy"),
        max_length=16,
        default=DeploymentImmediacyChoices.ON_DEMAND,
        choices=DeploymentImmediacyChoices,
    )

    clone_fields = (
        "aci_endpoint_group",
        "dcim_interface",
        "binding_type",
        "mode",
        "deployment_immediacy",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Static Port Binding")
        verbose_name_plural = _("ACI Static Port Bindings")
        ordering = ("aci_endpoint_group", "dcim_interface", "encap_vlan")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_endpoint_group", "dcim_interface", "encap_vlan"),
                name="netbox_cisco_aci_acistaticportbinding_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_endpoint_group} on {self.dcim_interface} (VLAN {self.encap_vlan})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acistaticportbinding", args=[self.pk])

    def save(self, *args, **kwargs):
        # Auto-derive APIC-compatible name from FK/encap if not provided.
        if not self.name and self.aci_endpoint_group_id and self.dcim_interface_id:
            epg_name = getattr(self.aci_endpoint_group, "name", "")
            iface_name = str(self.dcim_interface).replace("/", "_").replace(" ", "_")
            vlan = self.encap_vlan or 0
            candidate = f"spb_{epg_name}_{iface_name}_v{vlan}"
            # Strip any character APIC won't accept and cap at 64 chars.
            import re

            candidate = re.sub(r"[^A-Za-z0-9._:\-]", "_", candidate)
            self.name = candidate[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if (
            self.primary_encap_vlan is not None
            and self.encap_vlan is not None
            and self.primary_encap_vlan == self.encap_vlan
        ):
            raise ValidationError(
                {"primary_encap_vlan": _("Primary encap VLAN must differ from the encap VLAN.")}
            )

        if self.mode == StaticPortModeChoices.ACCESS_UNTAG and self.binding_type not in {
            StaticPortBindingTypeChoices.REGULAR,
            StaticPortBindingTypeChoices.PC,
            StaticPortBindingTypeChoices.VPC,
        }:
            raise ValidationError(
                {
                    "mode": _(
                        "`access-untagged` mode is only valid for regular, PC, or vPC bindings."
                    )
                }
            )

        if self.primary_encap_vlan is not None and self.aci_endpoint_group_id:
            is_useg = getattr(self.aci_endpoint_group, "is_useg", False)
            if not is_useg:
                raise ValidationError(
                    {
                        "primary_encap_vlan": _(
                            "Primary encap VLAN is only meaningful on a uSeg EPG."
                        )
                    }
                )
