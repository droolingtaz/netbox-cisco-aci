"""ACI Logical Interface Profile (``l3extLIfP``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import L3OutInterfaceTypeChoices
from ...constants import VLAN_ID_MAX, VLAN_ID_MIN
from ..base import ACIBaseModel

_ENCAP_REQUIRED_TYPES = {
    L3OutInterfaceTypeChoices.SUB_INTERFACE,
    L3OutInterfaceTypeChoices.SVI,
    L3OutInterfaceTypeChoices.FLOATING_SVI,
}


class ACILogicalInterfaceProfile(ACIBaseModel):
    """Logical Interface Profile (LIfP) attached to a Logical Node Profile."""

    aci_logical_node_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACILogicalNodeProfile",
        on_delete=models.CASCADE,
        related_name="logical_interface_profiles",
        verbose_name=_("Logical Node Profile"),
    )
    interface_type = models.CharField(
        verbose_name=_("Interface type"),
        max_length=16,
        default=L3OutInterfaceTypeChoices.ROUTED,
        choices=L3OutInterfaceTypeChoices,
    )
    encap_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("Encap VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
        blank=True,
        null=True,
        help_text=_("Required for sub-interface / SVI / floating-SVI."),
    )
    mtu = models.PositiveSmallIntegerField(
        verbose_name=_("MTU"),
        default=9000,
        validators=[MinValueValidator(64), MaxValueValidator(9216)],
    )

    clone_fields = ("aci_logical_node_profile", "interface_type", "mtu", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Logical Interface Profile")
        verbose_name_plural = _("ACI Logical Interface Profiles")
        ordering = ("aci_logical_node_profile", "name")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_logical_node_profile", "name"),
                name="netbox_cisco_aci_acilogicalinterfaceprofile_lnp_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_logical_node_profile} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilogicalinterfaceprofile", args=[self.pk])

    def clean(self) -> None:
        super().clean()

        if self.interface_type in _ENCAP_REQUIRED_TYPES and self.encap_vlan is None:
            raise ValidationError(
                {
                    "encap_vlan": _(
                        "Encap VLAN is required for sub-interface, SVI, or floating-SVI types."
                    )
                }
            )
        if self.interface_type == L3OutInterfaceTypeChoices.ROUTED and self.encap_vlan is not None:
            raise ValidationError(
                {"encap_vlan": _("Encap VLAN must be blank for routed interface types.")}
            )
