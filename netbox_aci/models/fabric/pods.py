"""ACI Pod — physical or virtual grouping of nodes inside a Fabric."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...constants import POD_ID_MAX, POD_ID_MIN
from ..base import ACIFabricBaseModel


class ACIPod(ACIFabricBaseModel):
    """A pod inside an ACI fabric.

    Pod IDs are unique inside a Fabric but not globally — the unique
    constraint below reflects that.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="pods",
        verbose_name=_("ACI Fabric"),
    )
    pod_id = models.PositiveSmallIntegerField(
        verbose_name=_("Pod ID"),
        validators=[MinValueValidator(POD_ID_MIN), MaxValueValidator(POD_ID_MAX)],
    )

    clone_fields = ("aci_fabric", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Pod")
        verbose_name_plural = _("ACI Pods")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "pod_id"),
                name="netbox_aci_acipod_fabric_podid_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_aci_acipod_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / Pod {self.pod_id} ({self.name})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:acipod", args=[self.pk])
