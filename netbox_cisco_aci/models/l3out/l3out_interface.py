"""ACI L3Out Interface (``l3extRsPathL3OutAtt``)."""

import ipaddress
import re

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIBaseModel


class ACIL3OutInterface(ACIBaseModel):
    """Binds a Logical Interface Profile to a physical ``dcim.Interface`` with IPs."""

    aci_logical_interface_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="interfaces",
        verbose_name=_("Logical Interface Profile"),
    )
    dcim_interface = models.ForeignKey(
        to="dcim.Interface",
        on_delete=models.PROTECT,
        related_name="aci_l3out_interfaces",
        verbose_name=_("NetBox Interface"),
    )
    ip_address = models.CharField(
        verbose_name=_("Primary IP/CIDR"),
        max_length=43,
        blank=True,
        help_text=_("Primary IPv4/IPv6 address with optional CIDR, e.g. 192.0.2.1/30."),
    )
    secondary_ip_addresses = models.JSONField(
        verbose_name=_("Secondary IP/CIDRs"),
        default=list,
        blank=True,
        help_text=_("List of additional IP/CIDR strings."),
    )
    mac_address = models.CharField(
        verbose_name=_("MAC address"),
        max_length=17,
        blank=True,
    )

    clone_fields = ("aci_logical_interface_profile", "dcim_interface", "mac_address")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI L3Out Interface")
        verbose_name_plural = _("ACI L3Out Interfaces")
        ordering = ("aci_logical_interface_profile", "dcim_interface")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_logical_interface_profile", "dcim_interface"),
                name="netbox_cisco_aci_acil3outinterface_lip_iface_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.dcim_interface} ({self.ip_address or 'no IP'})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acil3outinterface", args=[self.pk])

    def save(self, *args, **kwargs):
        # Auto-derive a deterministic, APIC-safe name when blank.
        if not self.name and self.aci_logical_interface_profile_id and self.dcim_interface_id:
            lip_name = getattr(self.aci_logical_interface_profile, "name", "")
            iface_name = str(self.dcim_interface).replace("/", "_").replace(" ", "_")
            candidate = f"l3if_{lip_name}_{iface_name}"
            candidate = re.sub(r"[^A-Za-z0-9._:\-]", "_", candidate)
            self.name = candidate[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if self.ip_address:
            try:
                ipaddress.ip_interface(self.ip_address)
            except ValueError as exc:
                raise ValidationError(
                    {"ip_address": _("Invalid IP/CIDR: %(err)s") % {"err": str(exc)}}
                ) from exc

        if self.secondary_ip_addresses:
            if not isinstance(self.secondary_ip_addresses, list):
                raise ValidationError(
                    {"secondary_ip_addresses": _("Must be a JSON list of strings.")}
                )
            for entry in self.secondary_ip_addresses:
                if not isinstance(entry, str):
                    raise ValidationError(
                        {"secondary_ip_addresses": _("Each entry must be a string.")}
                    )
                try:
                    ipaddress.ip_interface(entry)
                except ValueError as exc:
                    raise ValidationError(
                        {
                            "secondary_ip_addresses": _("Invalid secondary IP/CIDR %(v)s: %(err)s")
                            % {"v": entry, "err": str(exc)}
                        }
                    ) from exc
