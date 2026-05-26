"""ACI Logical Node (``l3extRsNodeL3OutAtt``)."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIBaseModel


class ACILogicalNode(ACIBaseModel):
    """Pin a single border-leaf node into a Logical Node Profile."""

    aci_logical_node_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalNodeProfile",
        on_delete=models.CASCADE,
        related_name="nodes",
        verbose_name=_("Logical Node Profile"),
    )
    aci_node = models.ForeignKey(
        to="netbox_cisco_aci.ACINode",
        on_delete=models.PROTECT,
        related_name="logical_node_attachments",
        verbose_name=_("ACI Node"),
    )
    router_id = models.GenericIPAddressField(
        protocol="IPv4",
        verbose_name=_("Router ID"),
        help_text=_("IPv4 router ID. APIC router IDs are IPv4-only."),
    )
    use_router_id_as_loopback = models.BooleanField(
        verbose_name=_("Use router ID as loopback"),
        default=True,
    )
    loopback_address = models.GenericIPAddressField(
        verbose_name=_("Loopback address"),
        blank=True,
        null=True,
        help_text=_("Only valid when 'Use router ID as loopback' is disabled."),
    )

    clone_fields = (
        "aci_logical_node_profile",
        "aci_node",
        "use_router_id_as_loopback",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Logical Node")
        verbose_name_plural = _("ACI Logical Nodes")
        ordering = ("aci_logical_node_profile", "aci_node")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_logical_node_profile", "aci_node"),
                name="netbox_cisco_aci_acilogicalnode_lnp_node_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_logical_node_profile", "router_id"),
                name="netbox_cisco_aci_acilogicalnode_lnp_routerid_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_node.name} ({self.router_id})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilogicalnode", args=[self.pk])

    def clean(self) -> None:
        super().clean()

        if self.use_router_id_as_loopback and self.loopback_address:
            raise ValidationError(
                {
                    "loopback_address": _(
                        "Loopback address must be empty when 'Use router ID as loopback' "
                        "is enabled."
                    )
                }
            )
        if not self.use_router_id_as_loopback and not self.loopback_address:
            raise ValidationError(
                {
                    "loopback_address": _(
                        "Loopback address is required when 'Use router ID as loopback' "
                        "is disabled."
                    )
                }
            )

        # Cross-fabric guard.
        if self.aci_node_id and self.aci_logical_node_profile_id:
            node_fabric = getattr(self.aci_node, "aci_fabric", None)
            lnp_fabric = getattr(self.aci_logical_node_profile, "aci_l3out", None)
            lnp_fabric = (
                getattr(getattr(lnp_fabric, "aci_tenant", None), "aci_fabric", None)
                if lnp_fabric
                else None
            )
            if node_fabric is not None and lnp_fabric is not None and node_fabric != lnp_fabric:
                raise ValidationError(
                    {
                        "aci_node": _(
                            "The selected node lives in a different fabric than the L3Out."
                        )
                    }
                )
