"""ACI Domain Binding (``fvRsDomAtt``) — Domain ↔ EPG binding."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import DeploymentImmediacyChoices, ResolutionImmediacyChoices
from ..base import ACIBaseModel


class ACIDomainBinding(ACIBaseModel):
    """Binds an EPG to a Domain with resolution / deployment immediacy."""

    aci_endpoint_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIEndpointGroup",
        on_delete=models.PROTECT,
        related_name="domain_bindings",
        verbose_name=_("ACI Endpoint Group"),
    )
    aci_domain = models.ForeignKey(
        to="netbox_cisco_aci.ACIDomain",
        on_delete=models.PROTECT,
        related_name="epg_bindings",
        verbose_name=_("ACI Domain"),
    )
    deployment_immediacy = models.CharField(
        verbose_name=_("Deployment immediacy"),
        max_length=16,
        default=DeploymentImmediacyChoices.ON_DEMAND,
        choices=DeploymentImmediacyChoices,
    )
    resolution_immediacy = models.CharField(
        verbose_name=_("Resolution immediacy"),
        max_length=16,
        default=ResolutionImmediacyChoices.ON_DEMAND,
        choices=ResolutionImmediacyChoices,
    )

    clone_fields = (
        "aci_endpoint_group",
        "aci_domain",
        "deployment_immediacy",
        "resolution_immediacy",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Domain Binding")
        verbose_name_plural = _("ACI Domain Bindings")
        ordering = ("aci_endpoint_group", "aci_domain")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_endpoint_group", "aci_domain"),
                name="netbox_cisco_aci_acidomainbinding_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_endpoint_group} \u2194 {self.aci_domain}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acidomainbinding", args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.name and self.aci_endpoint_group_id and self.aci_domain_id:
            epg_name = getattr(self.aci_endpoint_group, "name", "")
            dom_name = getattr(self.aci_domain, "name", "")
            import re

            candidate = f"dombnd_{epg_name}_{dom_name}"
            candidate = re.sub(r"[^A-Za-z0-9._:\-]", "_", candidate)
            self.name = candidate[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.aci_endpoint_group_id and self.aci_domain_id:
            epg_fabric_id = self.aci_endpoint_group.aci_tenant.aci_fabric_id
            dom_fabric_id = self.aci_domain.aci_fabric_id
            if epg_fabric_id != dom_fabric_id:
                raise ValidationError(
                    {"aci_domain": _("EPG and Domain must belong to the same ACI Fabric.")}
                )
