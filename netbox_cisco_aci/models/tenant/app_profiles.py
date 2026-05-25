"""ACI Application Profile (``fvAp``)."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..base import ACITenantBaseModel


class ACIAppProfile(ACITenantBaseModel):
    """An ACI Application Profile — container for EPGs inside a Tenant."""

    aci_tenant = models.ForeignKey(
        to="netbox_cisco_aci.ACITenant",
        on_delete=models.PROTECT,
        related_name="app_profiles",
        verbose_name=_("ACI Tenant"),
    )

    clone_fields = ("aci_tenant", "description")

    class Meta(ACITenantBaseModel.Meta):
        verbose_name = _("ACI Application Profile")
        verbose_name_plural = _("ACI Application Profiles")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_tenant", "name"),
                name="netbox_cisco_aci_aciappprofile_tenant_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_tenant} / AP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciappprofile", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_tenant.aci_fabric
