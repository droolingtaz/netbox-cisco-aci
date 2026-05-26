"""ACI Switch Profile (``infraNodeP``) and selector (``infraLeafS``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....choices import RangeAllChoices
from ....constants import NODE_ID_MAX, NODE_ID_MIN
from ...base import ACIFabricBaseModel


class ACISwitchProfile(ACIFabricBaseModel):
    """A Switch Profile (``infraNodeP``).

    Holds zero or more :class:`ACISwitchProfileSelector` rows that pick
    which leaves / spines the profile applies to, and is then attached
    to one or more Interface Profiles via
    :class:`netbox_cisco_aci.models.access.profiles.attachments.ACISwitchProfileInterfaceProfileAttachment`.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="switch_profiles",
        verbose_name=_("ACI Fabric"),
    )
    interface_profiles = models.ManyToManyField(
        to="netbox_cisco_aci.ACIInterfaceProfile",
        through="netbox_cisco_aci.ACISwitchProfileInterfaceProfileAttachment",
        related_name="switch_profiles",
        verbose_name=_("Interface Profiles"),
        blank=True,
    )

    clone_fields = ("aci_fabric", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Switch Profile")
        verbose_name_plural = _("ACI Switch Profiles")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_aciswprof_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / SwitchProfile {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciswitchprofile", args=[self.pk])


class ACISwitchProfileSelector(ACIFabricBaseModel):
    """A node selector inside a Switch Profile (``infraLeafS``).

    Either picks a single contiguous node-ID range (``selector_type=range``)
    or every node in the fabric (``selector_type=all``). APIC also supports
    an ``ALL_IN_POD`` flavour; not modelled yet.
    """

    switch_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACISwitchProfile",
        on_delete=models.CASCADE,
        related_name="selectors",
        verbose_name=_("Switch Profile"),
    )
    selector_type = models.CharField(
        verbose_name=_("Selector type"),
        max_length=8,
        default=RangeAllChoices.RANGE,
        choices=RangeAllChoices,
    )
    from_node_id = models.PositiveSmallIntegerField(
        verbose_name=_("From node ID"),
        blank=True,
        null=True,
        validators=[MinValueValidator(NODE_ID_MIN), MaxValueValidator(NODE_ID_MAX)],
    )
    to_node_id = models.PositiveSmallIntegerField(
        verbose_name=_("To node ID"),
        blank=True,
        null=True,
        validators=[MinValueValidator(NODE_ID_MIN), MaxValueValidator(NODE_ID_MAX)],
    )

    clone_fields = ("switch_profile", "selector_type", "from_node_id", "to_node_id")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Switch Profile Selector")
        verbose_name_plural = _("ACI Switch Profile Selectors")
        ordering = ("switch_profile", "from_node_id", "to_node_id")

    def __str__(self) -> str:
        if self.selector_type == RangeAllChoices.ALL:
            return f"{self.switch_profile.name} / all"
        return (
            f"{self.switch_profile.name} / "
            f"{self.selector_type}:{self.from_node_id}-{self.to_node_id}"
        )

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciswitchprofileselector", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.switch_profile.aci_fabric

    def clean(self) -> None:
        super().clean()
        if self.selector_type == RangeAllChoices.RANGE:
            if self.from_node_id is None or self.to_node_id is None:
                raise ValidationError(
                    _("`from_node_id` and `to_node_id` are required for range selectors.")
                )
            if self.from_node_id > self.to_node_id:
                raise ValidationError(
                    {
                        "to_node_id": _(
                            "`to_node_id` must be greater than or equal to `from_node_id`."
                        )
                    }
                )
        else:  # ALL
            if self.from_node_id is not None or self.to_node_id is not None:
                raise ValidationError(
                    _("`from_node_id` / `to_node_id` must be empty when selector_type='all'.")
                )
