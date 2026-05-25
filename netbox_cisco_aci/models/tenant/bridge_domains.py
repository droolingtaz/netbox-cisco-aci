"""ACI Bridge Domain (BD) and BD Subnet."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    BDL2UnknownUnicastChoices,
    BDL3UnknownMulticastChoices,
    BDMultiDestinationChoices,
)
from ...constants import COMMON_TENANT_NAME
from ..base import ACITenantBaseModel


class ACIBridgeDomain(ACITenantBaseModel):
    """An ACI Bridge Domain (``fvBD``).

    A BD must be backed by a VRF. The VRF may live in the same tenant
    or in the ``common`` tenant (per Cisco's import-from-common
    pattern). That second case is allowed only when ``aci_vrf`` is
    populated and resolves to a VRF whose tenant is named ``common``.
    """

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="bridge_domains",
        verbose_name=_("ACI Tenant"),
    )
    aci_vrf = models.ForeignKey(
        to="netbox_cisco_aci.ACIVRF",
        on_delete=models.PROTECT,
        related_name="bridge_domains",
        verbose_name=_("ACI VRF"),
        help_text=_("VRF backing this BD. May belong to the same tenant or to the common tenant."),
    )

    # L2/L3 forwarding policy
    unicast_routing_enabled = models.BooleanField(
        verbose_name=_("Unicast routing"),
        default=True,
        help_text=_(
            "Whether ACI acts as the L3 gateway for this BD. Best practice is "
            "to leave it on only when ACI is the gateway; otherwise leave it "
            "off (network-centric pattern)."
        ),
    )
    arp_flooding_enabled = models.BooleanField(
        verbose_name=_("ARP flooding"),
        default=False,
    )
    limit_ip_learn_to_subnets = models.BooleanField(
        verbose_name=_("Limit IP learning to subnets"),
        default=True,
        help_text=_("Best practice = enabled."),
    )
    l2_unknown_unicast = models.CharField(
        verbose_name=_("L2 unknown unicast"),
        max_length=16,
        default=BDL2UnknownUnicastChoices.PROXY,
        choices=BDL2UnknownUnicastChoices,
    )
    l3_unknown_multicast = models.CharField(
        verbose_name=_("L3 unknown multicast"),
        max_length=16,
        default=BDL3UnknownMulticastChoices.FLOOD,
        choices=BDL3UnknownMulticastChoices,
    )
    multi_destination_flooding = models.CharField(
        verbose_name=_("Multi-destination flooding"),
        max_length=16,
        default=BDMultiDestinationChoices.BD_FLOOD,
        choices=BDMultiDestinationChoices,
    )
    mac_address = models.CharField(
        verbose_name=_("Custom MAC address"),
        max_length=17,
        blank=True,
        help_text=_("Override the BD's default 00:22:BD:F8:19:FF."),
    )

    clone_fields = (
        "aci_tenant",
        "aci_vrf",
        "unicast_routing_enabled",
        "limit_ip_learn_to_subnets",
        "l2_unknown_unicast",
        "l3_unknown_multicast",
        "multi_destination_flooding",
        "description",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Bridge Domain")
        verbose_name_plural = _("ACI Bridge Domains")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_acibd_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant} / BD {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibridgedomain", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric

    def clean(self) -> None:
        super().clean()
        if self.aci_vrf_id and self.aci_tenant_id:
            vrf_tenant_id = getattr(self.aci_vrf, "aci_tenant_id", None)
            if vrf_tenant_id and vrf_tenant_id != self.aci_tenant_id:
                vrf_tenant_name = getattr(self.aci_vrf.aci_tenant, "name", "")
                if vrf_tenant_name != COMMON_TENANT_NAME:
                    raise ValidationError(
                        {
                            "aci_vrf": _(
                                "The VRF must belong to the same tenant as the "
                                "Bridge Domain, or to the `common` tenant."
                            )
                        }
                    )


class ACIBridgeDomainSubnet(ACITenantBaseModel):
    """A subnet attached to an ACI Bridge Domain.

    BDs may have multiple subnets, though Cisco best practice is one
    subnet per BD. The plugin does not enforce that — the Best-Practice
    audit reports on it instead.
    """

    aci_bridge_domain = models.ForeignKey(
        to="netbox_cisco_aci.ACIBridgeDomain",
        on_delete=models.CASCADE,
        related_name="subnets",
        verbose_name=_("ACI Bridge Domain"),
    )
    gateway_ip = models.CharField(
        verbose_name=_("Gateway IP"),
        max_length=64,
        help_text=_("Gateway IP in CIDR form, e.g. 10.0.0.1/24."),
    )
    nb_prefix = models.ForeignKey(
        to="ipam.Prefix",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        verbose_name=_("NetBox prefix"),
        help_text=_("Optional link to the corresponding NetBox ipam.Prefix."),
    )
    scope_public = models.BooleanField(
        verbose_name=_("Advertised externally"),
        default=False,
    )
    scope_shared = models.BooleanField(
        verbose_name=_("Shared between VRFs"),
        default=False,
    )
    scope_private = models.BooleanField(
        verbose_name=_("Private to VRF"),
        default=True,
    )
    is_primary = models.BooleanField(
        verbose_name=_("Primary"),
        default=False,
    )

    clone_fields = (
        "aci_bridge_domain",
        "scope_public",
        "scope_shared",
        "scope_private",
    )

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI BD Subnet")
        verbose_name_plural = _("ACI BD Subnets")
        ordering = ("aci_bridge_domain", "gateway_ip")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_bridge_domain", "gateway_ip"),
                name="netbox_cisco_aci_acibdsubnet_bd_gw_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_bridge_domain} / {self.gateway_ip}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acibridgedomainsubnet", args=[self.pk])

    @property
    def aci_tenant(self):
        return self.aci_bridge_domain.aci_tenant

    @property
    def aci_fabric(self):
        return self.aci_bridge_domain.aci_tenant.aci_fabric
