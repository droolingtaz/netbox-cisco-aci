"""ACI Filter (``vzFilter``) and Filter Entry (``vzEntry``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
)
from ..base import ACIBaseModel, ACITenantBaseModel


class ACIFilter(ACITenantBaseModel):
    """A reusable L2/L3/L4 match definition.

    Filters can be defined in the ``common`` tenant and referenced from
    other tenants — uniqueness is per tenant.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="filters",
        verbose_name=_("ACI Tenant"),
    )

    clone_fields = ("aci_tenant", "description")

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Filter")
        verbose_name_plural = _("ACI Filters")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acifilter_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acifilter", args=[self.pk])


class ACIFilterEntry(ACIBaseModel):
    """A single match clause inside a filter.

    Cisco's filter-entry model is a wide flat row that covers L2 (ARP),
    L3 (IPv4/IPv6/etc.), and L4 (TCP/UDP ports, TCP flags, ICMP types,
    fragmentation). Each entry corresponds to one ``vzEntry`` MO.
    """

    aci_filter = models.ForeignKey(
        to="netbox_cisco_aci.ACIFilter",
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name=_("ACI Filter"),
    )
    ether_type = models.CharField(
        verbose_name=_("EtherType"),
        max_length=16,
        default=ContractFilterEntryEtherTypeChoices.UNSPECIFIED,
        choices=ContractFilterEntryEtherTypeChoices,
    )
    ip_protocol = models.CharField(
        verbose_name=_("IP protocol"),
        max_length=16,
        blank=True,
        default=ContractFilterEntryIPProtocolChoices.UNSPECIFIED,
        choices=ContractFilterEntryIPProtocolChoices,
    )
    source_port_from = models.PositiveSmallIntegerField(
        verbose_name=_("Source port (from)"),
        blank=True,
        null=True,
        validators=(MinValueValidator(0), MaxValueValidator(65535)),
    )
    source_port_to = models.PositiveSmallIntegerField(
        verbose_name=_("Source port (to)"),
        blank=True,
        null=True,
        validators=(MinValueValidator(0), MaxValueValidator(65535)),
    )
    destination_port_from = models.PositiveSmallIntegerField(
        verbose_name=_("Destination port (from)"),
        blank=True,
        null=True,
        validators=(MinValueValidator(0), MaxValueValidator(65535)),
    )
    destination_port_to = models.PositiveSmallIntegerField(
        verbose_name=_("Destination port (to)"),
        blank=True,
        null=True,
        validators=(MinValueValidator(0), MaxValueValidator(65535)),
    )
    tcp_rules = models.CharField(
        verbose_name=_("TCP rules"),
        max_length=64,
        blank=True,
        help_text=_("Comma-separated TCP flag rules (e.g. ``est,syn``)."),
    )
    match_only_fragments = models.BooleanField(
        verbose_name=_("Match only fragments"),
        default=False,
    )
    arp_opcode = models.CharField(
        verbose_name=_("ARP opcode"),
        max_length=8,
        blank=True,
        help_text=_("Only meaningful when ether_type=arp. ``req`` or ``reply``."),
    )
    stateful = models.BooleanField(
        verbose_name=_("Stateful"),
        default=False,
    )
    icmp_v4_type = models.CharField(
        verbose_name=_("ICMPv4 type"),
        max_length=16,
        blank=True,
    )
    icmp_v6_type = models.CharField(
        verbose_name=_("ICMPv6 type"),
        max_length=16,
        blank=True,
    )

    clone_fields = (
        "aci_filter",
        "ether_type",
        "ip_protocol",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Filter Entry")
        verbose_name_plural = _("ACI Filter Entries")
        ordering = ("aci_filter", "name")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_filter", "name"),
                name="netbox_cisco_aci_acifilterentry_filter_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_filter.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acifilterentry", args=[self.pk])

    @property
    def aci_tenant(self):
        return self.aci_filter.aci_tenant

    def clean(self) -> None:
        super().clean()
        errors: dict[str, str] = {}

        # Source/destination port pair: if either is set both must be set, and from <= to.
        for label, lo_field, hi_field in (
            ("source", "source_port_from", "source_port_to"),
            ("destination", "destination_port_from", "destination_port_to"),
        ):
            lo = getattr(self, lo_field)
            hi = getattr(self, hi_field)
            if (lo is None) != (hi is None):
                errors[lo_field if lo is None else hi_field] = _(
                    f"Both endpoints of the {label} port range must be set together."
                )
            elif lo is not None and hi is not None and lo > hi:
                errors[hi_field] = _(f"{label.capitalize()} port `to` must be >= `from`.")

        # Port fields only valid for TCP/UDP.
        port_fields_set = any(
            getattr(self, f) is not None
            for f in (
                "source_port_from",
                "source_port_to",
                "destination_port_from",
                "destination_port_to",
            )
        )
        if port_fields_set and self.ip_protocol not in (
            ContractFilterEntryIPProtocolChoices.TCP,
            ContractFilterEntryIPProtocolChoices.UDP,
        ):
            errors["ip_protocol"] = _("Port fields are only valid when ip_protocol is TCP or UDP.")

        # ARP opcode only valid when ether_type=arp.
        if self.arp_opcode and self.ether_type != ContractFilterEntryEtherTypeChoices.ARP:
            errors["arp_opcode"] = _("ARP opcode is only meaningful when ether_type is ARP.")

        # ICMPv4 type only valid when ip_protocol=icmp.
        if self.icmp_v4_type and self.ip_protocol != ContractFilterEntryIPProtocolChoices.ICMP:
            errors["icmp_v4_type"] = _("ICMPv4 type is only valid when ip_protocol is ICMP.")

        # ICMPv6 type only valid when ip_protocol=icmpv6.
        if self.icmp_v6_type and self.ip_protocol != ContractFilterEntryIPProtocolChoices.ICMPV6:
            errors["icmp_v6_type"] = _("ICMPv6 type is only valid when ip_protocol is ICMPv6.")

        if errors:
            raise ValidationError(errors)
