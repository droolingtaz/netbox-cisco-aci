"""ACI L3Out Static Route + Next Hop (``ipRouteP`` / ``ipNexthopP``)."""

import ipaddress
import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import StaticRouteNextHopTypeChoices
from ..base import ACIBaseModel


class ACIL3OutStaticRoute(ACIBaseModel):
    """Per-node static route under an ACI Logical Node (``ipRouteP``)."""

    aci_logical_node = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalNode",
        on_delete=models.CASCADE,
        related_name="static_routes",
        verbose_name=_("ACI Logical Node"),
    )
    prefix = models.CharField(
        verbose_name=_("Prefix"),
        max_length=43,
        help_text=_(
            "IPv4 or IPv6 network with prefix length (e.g. 0.0.0.0/0, 10.50.0.0/16, 2001:db8::/32)."
        ),
    )
    track_policy = models.CharField(
        verbose_name=_("Track policy"),
        max_length=64,
        blank=True,
        help_text=_("Optional IP SLA track policy name (APIC string reference)."),
    )
    preference = models.PositiveSmallIntegerField(
        verbose_name=_("Preference"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
        help_text=_("Administrative distance (1–255)."),
    )
    route_controls = models.JSONField(
        verbose_name=_("Route controls"),
        default=list,
        blank=True,
        help_text=_(
            "JSON list of route-control tokens. Recognised tokens: "
            "``bfd`` (BFD tracking), ``bfd.only``. Any string is accepted."
        ),
    )

    clone_fields = (
        "aci_logical_node",
        "prefix",
        "track_policy",
        "preference",
        "route_controls",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI L3Out Static Route")
        verbose_name_plural = _("ACI L3Out Static Routes")
        ordering = ("aci_logical_node", "prefix")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_logical_node", "prefix"),
                name="netbox_cisco_aci_acil3outstaticroute_node_prefix_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_logical_node.name} -> {self.prefix}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acil3outstaticroute", args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.name:
            node = getattr(self.aci_logical_node, "name", str(self.aci_logical_node_id))
            slug = re.sub(r"[^A-Za-z0-9._:\-]", "_", f"route_{node}_{self.prefix}")
            self.name = slug[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if self.prefix:
            try:
                ipaddress.ip_network(self.prefix, strict=False)
            except ValueError as exc:
                raise ValidationError(
                    {"prefix": _("Invalid prefix: %(err)s") % {"err": str(exc)}}
                ) from exc

        if self.route_controls and not isinstance(self.route_controls, list):
            raise ValidationError({"route_controls": _("Must be a JSON list of strings.")})


class ACIL3OutStaticRouteNextHop(ACIBaseModel):
    """Per-route next-hop entry under an L3Out static route (``ipNexthopP``)."""

    aci_static_route = models.ForeignKey(
        to="netbox_cisco_aci.ACIL3OutStaticRoute",
        on_delete=models.CASCADE,
        related_name="next_hops",
        verbose_name=_("ACI Static Route"),
    )
    nexthop_address = models.CharField(
        verbose_name=_("Next-hop address"),
        max_length=43,
        blank=True,
        help_text=_(
            "IPv4 or IPv6 address (no CIDR). "
            "Leave blank when nexthop_type is ``none`` (null route)."
        ),
    )
    nexthop_type = models.CharField(
        verbose_name=_("Next-hop type"),
        max_length=16,
        default=StaticRouteNextHopTypeChoices.PREFIX,
        choices=StaticRouteNextHopTypeChoices,
        help_text=_(
            "``prefix`` installs a normal next-hop; ``none`` installs a null (discard) route."
        ),
    )
    preference = models.PositiveSmallIntegerField(
        verbose_name=_("Preference"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        help_text=_(
            "Per-next-hop preference for ECMP weighting (0–255). "
            "0 means inherit from the parent static route."
        ),
    )

    clone_fields = (
        "aci_static_route",
        "nexthop_address",
        "nexthop_type",
        "preference",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI L3Out Static Route Next Hop")
        verbose_name_plural = _("ACI L3Out Static Route Next Hops")
        ordering = ("aci_static_route", "nexthop_address")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_static_route", "nexthop_address"),
                name="netbox_cisco_aci_acil3outstaticroutenexthop_route_addr_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_static_route} via {self.nexthop_address or 'null'}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acil3outstaticroutenexthop", args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.name:
            addr = self.nexthop_address or "null"
            slug = re.sub(r"[^A-Za-z0-9._:\-]", "_", f"nh_{addr}")
            self.name = slug[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if self.nexthop_type == StaticRouteNextHopTypeChoices.NONE:
            if self.nexthop_address:
                raise ValidationError(
                    {
                        "nexthop_address": _(
                            "Next-hop address must be blank for a null-route (nexthop_type='none')."
                        )
                    }
                )
        else:
            # prefix type
            if not self.nexthop_address:
                raise ValidationError(
                    {
                        "nexthop_address": _(
                            "Next-hop address is required when nexthop_type is 'prefix'."
                        )
                    }
                )
            try:
                ipaddress.ip_address(self.nexthop_address)
            except ValueError as exc:
                raise ValidationError(
                    {"nexthop_address": _("Invalid IP address: %(err)s") % {"err": str(exc)}}
                ) from exc
