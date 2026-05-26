"""ACI Contract Relation (``vzRsCons`` / ``vzRsProv``)."""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import ContractRelationRoleChoices
from ...constants import COMMON_TENANT_NAME
from ..base import ACIBaseModel


class ACIContractRelation(ACIBaseModel):
    """Provider / consumer relationship from an EPG / ESG / External EPG to a Contract.

    Exactly one of ``aci_endpoint_group`` / ``aci_endpoint_security_group``
    / ``aci_external_epg`` must be set. The Contract's tenant must match the
    target's tenant or be the ``common`` tenant.
    """

    aci_contract = models.ForeignKey(
        to="netbox_cisco_aci.ACIContract",
        on_delete=models.CASCADE,
        related_name="relations",
        verbose_name=_("ACI Contract"),
    )
    aci_endpoint_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIEndpointGroup",
        on_delete=models.CASCADE,
        related_name="contract_relations",
        blank=True,
        null=True,
        verbose_name=_("ACI Endpoint Group"),
    )
    aci_endpoint_security_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIEndpointSecurityGroup",
        on_delete=models.CASCADE,
        related_name="contract_relations",
        blank=True,
        null=True,
        verbose_name=_("ACI Endpoint Security Group"),
    )
    aci_external_epg = models.ForeignKey(
        to="netbox_cisco_aci.ACIExternalEPG",
        on_delete=models.CASCADE,
        related_name="contract_relations",
        blank=True,
        null=True,
        verbose_name=_("ACI External EPG"),
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=16,
        choices=ContractRelationRoleChoices,
    )

    clone_fields = (
        "aci_contract",
        "aci_endpoint_group",
        "aci_endpoint_security_group",
        "aci_external_epg",
        "role",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Contract Relation")
        verbose_name_plural = _("ACI Contract Relations")
        ordering = ("aci_contract", "role")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_contract", "aci_endpoint_group", "role"),
                condition=Q(aci_endpoint_group__isnull=False),
                name="netbox_cisco_aci_acicontractrelation_epg_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_contract", "aci_endpoint_security_group", "role"),
                condition=Q(aci_endpoint_security_group__isnull=False),
                name="netbox_cisco_aci_acicontractrelation_esg_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_contract", "aci_external_epg", "role"),
                condition=Q(aci_external_epg__isnull=False),
                name="netbox_cisco_aci_acicontractrelation_extepg_unique",
            ),
        )

    def __str__(self) -> str:
        target = (
            self.aci_endpoint_group
            or self.aci_endpoint_security_group
            or self.aci_external_epg
        )
        target_name = target.name if target is not None else "<unattached>"
        return f"{self.aci_contract.name} {self.role} {target_name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acicontractrelation", args=[self.pk])

    @property
    def target(self):
        return (
            self.aci_endpoint_group
            or self.aci_endpoint_security_group
            or self.aci_external_epg
        )

    def clean(self) -> None:
        super().clean()
        errors: dict[str, str] = {}

        # XOR: exactly one of EPG / ESG / External EPG must be set.
        has_epg = self.aci_endpoint_group_id is not None
        has_esg = self.aci_endpoint_security_group_id is not None
        has_extepg = self.aci_external_epg_id is not None
        set_count = sum((has_epg, has_esg, has_extepg))
        if set_count != 1:
            errors["aci_endpoint_group"] = _(
                "Exactly one of EPG, ESG, or External EPG must be set on a contract relation."
            )

        if errors:
            raise ValidationError(errors)

        contract_tenant = getattr(self.aci_contract, "aci_tenant", None)
        contract_tenant_name = getattr(contract_tenant, "name", "")
        target_tenant_id = None
        if has_epg:
            target_tenant_id = getattr(self.aci_endpoint_group, "aci_tenant_id", None)
        elif has_esg:
            target_tenant_id = getattr(
                self.aci_endpoint_security_group, "aci_tenant_id", None
            )
        else:
            ext = self.aci_external_epg
            l3out = getattr(ext, "aci_l3out", None)
            target_tenant_id = getattr(l3out, "aci_tenant_id", None) if l3out else None

        if (
            contract_tenant is not None
            and target_tenant_id is not None
            and contract_tenant.id != target_tenant_id
            and contract_tenant_name != COMMON_TENANT_NAME
        ):
            raise ValidationError(
                {
                    "aci_contract": _(
                        "Contract must belong to the same tenant as the "
                        "EPG/ESG/External EPG, or to the `common` tenant."
                    )
                }
            )
