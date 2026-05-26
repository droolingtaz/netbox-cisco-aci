"""ACI LACP / port-channel policy (``lacpLagPol``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import LACPModeChoices
from ....constants import LACP_LINKS_MAX, LACP_LINKS_MIN
from ...base import ACIFabricBaseModel


class ACILACPInterfacePolicy(ACIFabricBaseModel):
    """A LACP / port-channel policy.

    Encodes the ``lacpLagPol`` settings (mode, link bounds, control
    flags). The control flags map 1:1 to the ``ctrl`` bitmask APIC ships
    as a comma-separated list.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="lacp_policies",
        verbose_name=_("ACI Fabric"),
    )
    mode = models.CharField(
        verbose_name=_("Mode"),
        max_length=24,
        default=LACPModeChoices.OFF,
        choices=LACPModeChoices,
    )
    min_links = models.PositiveSmallIntegerField(
        verbose_name=_("Minimum links"),
        default=1,
        validators=[MinValueValidator(LACP_LINKS_MIN), MaxValueValidator(LACP_LINKS_MAX)],
    )
    max_links = models.PositiveSmallIntegerField(
        verbose_name=_("Maximum links"),
        default=16,
        validators=[MinValueValidator(LACP_LINKS_MIN), MaxValueValidator(LACP_LINKS_MAX)],
    )
    control_fast_select_hot_standby = models.BooleanField(
        verbose_name=_("Fast select hot standby"),
        default=True,
    )
    control_graceful_convergence = models.BooleanField(
        verbose_name=_("Graceful convergence"),
        default=True,
    )
    control_load_defer = models.BooleanField(
        verbose_name=_("Load defer"),
        default=False,
    )
    control_suspend_individual_port = models.BooleanField(
        verbose_name=_("Suspend individual port"),
        default=True,
    )
    control_symmetric_hashing = models.BooleanField(
        verbose_name=_("Symmetric hashing"),
        default=False,
    )

    clone_fields = (
        "aci_fabric",
        "mode",
        "min_links",
        "max_links",
        "description",
    )

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI LACP Interface Policy")
        verbose_name_plural = _("ACI LACP Interface Policies")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acilacppol_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / LACP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilacpinterfacepolicy", args=[self.pk])

    def clean(self) -> None:
        super().clean()
        if (
            self.min_links is not None
            and self.max_links is not None
            and self.min_links > self.max_links
        ):
            raise ValidationError(
                {"max_links": _("`max_links` must be greater than or equal to `min_links`.")}
            )
