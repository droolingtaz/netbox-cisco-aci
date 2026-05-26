"""ACI BGP Peer (``bgpPeerP``)."""

import ipaddress

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIBaseModel


class ACIBGPPeer(ACIBaseModel):
    """BGP peer attached at either LIP or LNP scope."""

    aci_logical_interface_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="bgp_peers",
        blank=True,
        null=True,
        verbose_name=_("Logical Interface Profile"),
    )
    aci_logical_node_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalNodeProfile",
        on_delete=models.CASCADE,
        related_name="bgp_peers",
        blank=True,
        null=True,
        verbose_name=_("Logical Node Profile"),
    )
    peer_address = models.CharField(
        verbose_name=_("Peer address"),
        max_length=43,
        help_text=_("IPv4 or IPv6 address of the remote peer (no CIDR)."),
    )
    remote_asn = models.PositiveBigIntegerField(
        verbose_name=_("Remote ASN"),
        validators=[MinValueValidator(1), MaxValueValidator(4_294_967_295)],
    )
    local_asn = models.PositiveBigIntegerField(
        verbose_name=_("Local ASN override"),
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(4_294_967_295)],
    )
    ebgp_multihop_ttl = models.PositiveSmallIntegerField(
        verbose_name=_("eBGP multihop TTL"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(255)],
    )
    password = models.CharField(
        verbose_name=_("MD5 password"),
        max_length=64,
        blank=True,
        help_text=_("APIC stores this as the MD5 auth secret on the BGP policy."),
    )
    bgp_controls = models.JSONField(
        verbose_name=_("BGP controls"),
        default=list,
        blank=True,
        help_text=_(
            "Tokens: allow-self-as, as-override, disable-peer-as-check, next-hop-self, "
            "send-com, send-ext-com."
        ),
    )
    peer_controls = models.JSONField(
        verbose_name=_("Peer controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: bfd, disable-conn-check."),
    )
    address_family_controls = models.JSONField(
        verbose_name=_("Address family controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: send-com-ext, send-com."),
    )
    private_asn_controls = models.JSONField(
        verbose_name=_("Private ASN controls"),
        default=list,
        blank=True,
        help_text=_("Tokens: remove-exclusive, remove-all, replace-as."),
    )

    clone_fields = (
        "aci_logical_interface_profile",
        "aci_logical_node_profile",
        "remote_asn",
        "local_asn",
        "ebgp_multihop_ttl",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI BGP Peer")
        verbose_name_plural = _("ACI BGP Peers")
        ordering = ("peer_address",)
        constraints = (
            models.UniqueConstraint(
                fields=("aci_logical_interface_profile", "peer_address"),
                condition=Q(aci_logical_interface_profile__isnull=False),
                name="netbox_cisco_aci_acibgppeer_lip_addr_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_logical_node_profile", "peer_address"),
                condition=Q(aci_logical_node_profile__isnull=False),
                name="netbox_cisco_aci_acibgppeer_lnp_addr_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.peer_address} AS{self.remote_asn}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibgppeer", args=[self.pk])

    def clean(self) -> None:
        super().clean()

        has_lip = self.aci_logical_interface_profile_id is not None
        has_lnp = self.aci_logical_node_profile_id is not None
        if has_lip == has_lnp:
            raise ValidationError(
                _(
                    "Exactly one of Logical Interface Profile or Logical Node Profile "
                    "must be set on a BGP peer."
                )
            )

        if self.peer_address:
            try:
                ipaddress.ip_address(self.peer_address)
            except ValueError as exc:
                raise ValidationError(
                    {"peer_address": _("Invalid IP address: %(err)s") % {"err": str(exc)}}
                ) from exc
