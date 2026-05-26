"""ACI Logical Node Profile (``l3extLNodeP``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACIBaseModel


class ACILogicalNodeProfile(ACIBaseModel):
    """Group of border-leaf nodes carrying a shared L3Out attachment."""

    aci_l3out = models.ForeignKey(
        to="netbox_cisco_aci.ACIL3Out",
        on_delete=models.CASCADE,
        related_name="logical_node_profiles",
        verbose_name=_("ACI L3Out"),
    )
    target_dscp = models.CharField(
        verbose_name=_("Target DSCP"),
        max_length=32,
        blank=True,
    )

    clone_fields = ("aci_l3out", "target_dscp", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Logical Node Profile")
        verbose_name_plural = _("ACI Logical Node Profiles")
        ordering = ("aci_l3out", "name")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_l3out", "name"),
                name="netbox_cisco_aci_acilogicalnodeprofile_l3out_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_l3out} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acilogicalnodeprofile", args=[self.pk])

    @property
    def aci_tenant(self):
        return self.aci_l3out.aci_tenant
