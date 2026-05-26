"""ACI Link Level interface policy (``fabricHIfPol``)."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import (
    LinkLevelAutoNegChoices,
    LinkLevelFECChoices,
    LinkLevelSpeedChoices,
)
from ....constants import LINK_DEBOUNCE_MAX, LINK_DEBOUNCE_MIN
from ...base import ACIFabricBaseModel


class ACILinkLevelPolicy(ACIFabricBaseModel):
    """A Link Level interface policy.

    Pins per-interface PHY characteristics (speed, auto-negotiation,
    debounce, FEC). Referenced by Interface Policy Groups via the
    ``link_level_policy`` FK.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="link_level_policies",
        verbose_name=_("ACI Fabric"),
    )
    speed = models.CharField(
        verbose_name=_("Speed"),
        max_length=16,
        default=LinkLevelSpeedChoices.INHERIT,
        choices=LinkLevelSpeedChoices,
    )
    auto_negotiation = models.CharField(
        verbose_name=_("Auto-negotiation"),
        max_length=8,
        default=LinkLevelAutoNegChoices.ON,
        choices=LinkLevelAutoNegChoices,
    )
    link_debounce_interval_ms = models.PositiveIntegerField(
        verbose_name=_("Link debounce (ms)"),
        default=100,
        validators=[
            MinValueValidator(LINK_DEBOUNCE_MIN),
            MaxValueValidator(LINK_DEBOUNCE_MAX),
        ],
    )
    fec_mode = models.CharField(
        verbose_name=_("FEC mode"),
        max_length=16,
        default=LinkLevelFECChoices.INHERIT,
        choices=LinkLevelFECChoices,
    )

    clone_fields = (
        "aci_fabric",
        "speed",
        "auto_negotiation",
        "link_debounce_interval_ms",
        "fec_mode",
        "description",
    )

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Link Level Policy")
        verbose_name_plural = _("ACI Link Level Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acilinklevelpol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / LinkLevel {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilinklevelpolicy", args=[self.pk])
