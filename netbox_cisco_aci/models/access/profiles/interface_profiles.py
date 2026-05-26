"""ACI Interface Profile (``infraAccPortP``) and selector (``infraHPortS``)."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ....constants import MODULE_ID_MAX, MODULE_ID_MIN, PORT_ID_MAX, PORT_ID_MIN
from ...base import ACIFabricBaseModel


class ACIInterfaceProfile(ACIFabricBaseModel):
    """An Interface Profile (``infraAccPortP``).

    Container for one or more :class:`ACIInterfaceProfileSelector`
    rows that pin a Policy Group onto a contiguous module/port range.
    Attached to Switch Profiles via the through model so a single port
    profile can apply to many leaves.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="interface_profiles",
        verbose_name=_("ACI Fabric"),
    )

    clone_fields = ("aci_fabric", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Interface Profile")
        verbose_name_plural = _("ACI Interface Profiles")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_aciintfprof_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / InterfaceProfile {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciinterfaceprofile", args=[self.pk])


class ACIInterfaceProfileSelector(ACIFabricBaseModel):
    """An interface selector (``infraHPortS``).

    Targets a contiguous (module, port) range on every node the parent
    Interface Profile applies to, and pins a single Interface Policy
    Group on it.
    """

    interface_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACIInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="selectors",
        verbose_name=_("Interface Profile"),
    )
    policy_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIInterfacePolicyGroup",
        on_delete=models.PROTECT,
        related_name="selectors",
        verbose_name=_("Policy Group"),
        blank=True,
        null=True,
    )
    from_module = models.PositiveSmallIntegerField(
        verbose_name=_("From module"),
        default=1,
        validators=[MinValueValidator(MODULE_ID_MIN), MaxValueValidator(MODULE_ID_MAX)],
    )
    from_port = models.PositiveSmallIntegerField(
        verbose_name=_("From port"),
        validators=[MinValueValidator(PORT_ID_MIN), MaxValueValidator(PORT_ID_MAX)],
    )
    to_module = models.PositiveSmallIntegerField(
        verbose_name=_("To module"),
        default=1,
        validators=[MinValueValidator(MODULE_ID_MIN), MaxValueValidator(MODULE_ID_MAX)],
    )
    to_port = models.PositiveSmallIntegerField(
        verbose_name=_("To port"),
        validators=[MinValueValidator(PORT_ID_MIN), MaxValueValidator(PORT_ID_MAX)],
    )

    clone_fields = (
        "interface_profile",
        "policy_group",
        "from_module",
        "from_port",
        "to_module",
        "to_port",
    )

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Interface Profile Selector")
        verbose_name_plural = _("ACI Interface Profile Selectors")
        ordering = ("interface_profile", "from_module", "from_port")

    def __str__(self) -> str:
        return (
            f"{self.interface_profile.name} / "
            f"{self.from_module}/{self.from_port}-{self.to_module}/{self.to_port}"
        )

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciinterfaceprofileselector", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.interface_profile.aci_fabric

    def clean(self) -> None:
        super().clean()
        # Lexicographic ordering on (module, port).
        if (self.from_module, self.from_port) > (self.to_module, self.to_port):
            raise ValidationError(_("(from_module, from_port) must be <= (to_module, to_port)."))
        # Cross-fabric guard: policy group must belong to the same fabric
        # as the interface profile.
        if self.policy_group_id and self.interface_profile_id:
            pg_fabric_id = self.policy_group.aci_fabric_id
            ip_fabric_id = self.interface_profile.aci_fabric_id
            if pg_fabric_id != ip_fabric_id:
                raise ValidationError(
                    {
                        "policy_group": _(
                            "Policy Group belongs to a different Fabric than the Interface Profile."
                        )
                    }
                )
