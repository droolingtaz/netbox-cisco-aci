"""ACI Attachable Access Entity Profiles (AAEPs) and their associations.

Phase 3 introduces three models:

* :class:`ACIAAEP` \u2014 the AAEP itself (``infraAttEntityP``).
* :class:`ACIAAEPDomainAssociation` \u2014 explicit through model linking
  AAEPs to Domains (``infraRsDomP``). Kept as a real model rather than
  a M2M auto-through so future per-association columns (e.g. priority,
  notes) have somewhere to live.
* :class:`ACIAAEPEPGMapping` \u2014 the "AAEP \u2192 EPG" mapping (``infraRsFuncToEpg``)
  with encap VLAN, mode (trunk / access tagged / access untagged) and
  the EPG itself. This is what lets ACI program ports against an AAEP
  with EPG state inherited from this mapping (the alternative to
  per-port static bindings).
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import StaticPortModeChoices
from ...constants import VLAN_ID_MAX, VLAN_ID_MIN
from ..base import ACIFabricBaseModel


class ACIAAEP(ACIFabricBaseModel):
    """An Attachable Access Entity Profile (``infraAttEntityP``)."""

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="aaeps",
        verbose_name=_("ACI Fabric"),
    )
    enable_infra_vlan = models.BooleanField(
        verbose_name=_("Enable infra VLAN"),
        default=False,
        help_text=_("Extends the infra-VLAN to interfaces using this AAEP."),
    )
    domains = models.ManyToManyField(
        to="netbox_cisco_aci.ACIDomain",
        through="netbox_cisco_aci.ACIAAEPDomainAssociation",
        related_name="aaeps",
        verbose_name=_("Domains"),
        blank=True,
    )

    clone_fields = ("aci_fabric", "enable_infra_vlan", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI AAEP")
        verbose_name_plural = _("ACI AAEPs")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_aciaaep_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / AAEP {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciaaep", args=[self.pk])


class ACIAAEPDomainAssociation(models.Model):
    """Through model linking an AAEP to a Domain (``infraRsDomP``)."""

    aci_aaep = models.ForeignKey(
        to="netbox_cisco_aci.ACIAAEP",
        on_delete=models.CASCADE,
        related_name="domain_associations",
        verbose_name=_("AAEP"),
    )
    aci_domain = models.ForeignKey(
        to="netbox_cisco_aci.ACIDomain",
        on_delete=models.PROTECT,
        related_name="aaep_associations",
        verbose_name=_("Domain"),
    )

    class Meta:
        verbose_name = _("ACI AAEP-Domain Association")
        verbose_name_plural = _("ACI AAEP-Domain Associations")
        ordering = ("aci_aaep", "aci_domain")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_aaep", "aci_domain"),
                name="netbox_cisco_aci_aciaaepdomain_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_aaep.name} \u2192 {self.aci_domain.name}"

    def clean(self) -> None:
        super().clean()
        if self.aci_aaep_id and self.aci_domain_id:
            if self.aci_aaep.aci_fabric_id != self.aci_domain.aci_fabric_id:
                raise ValidationError(
                    _(
                        "AAEP and Domain must belong to the same Fabric. "
                        "AAEP is in %(a)s, Domain is in %(d)s."
                    )
                    % {
                        "a": self.aci_aaep.aci_fabric.name,
                        "d": self.aci_domain.aci_fabric.name,
                    }
                )


class ACIAAEPEPGMapping(ACIFabricBaseModel):
    """AAEP \u2192 EPG mapping (``infraRsFuncToEpg``).

    Each mapping pins an EPG onto an AAEP with an encap VLAN and a
    switching mode. ACI then programs every interface attached to the
    AAEP with that EPG state (in addition to any per-port static
    bindings).
    """

    aci_aaep = models.ForeignKey(
        to="netbox_cisco_aci.ACIAAEP",
        on_delete=models.CASCADE,
        related_name="epg_mappings",
        verbose_name=_("AAEP"),
    )
    aci_endpoint_group = models.ForeignKey(
        to="netbox_cisco_aci.ACIEndpointGroup",
        on_delete=models.PROTECT,
        related_name="aaep_mappings",
        verbose_name=_("Endpoint Group"),
    )
    encap_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("Encap VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
    )
    mode = models.CharField(
        verbose_name=_("Mode"),
        max_length=16,
        default=StaticPortModeChoices.TRUNK,
        choices=StaticPortModeChoices,
    )

    clone_fields = ("aci_aaep", "aci_endpoint_group", "mode")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI AAEP-EPG Mapping")
        verbose_name_plural = _("ACI AAEP-EPG Mappings")
        ordering = ("aci_aaep", "encap_vlan")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_aaep", "aci_endpoint_group", "encap_vlan"),
                name="netbox_cisco_aci_aciaaepepgmap_unique",
            ),
        )

    def __str__(self) -> str:
        return (
            f"{self.aci_aaep.name} \u2192 EPG {self.aci_endpoint_group.name} "
            f"(VLAN {self.encap_vlan})"
        )

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:aciaaepepgmapping", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_aaep.aci_fabric

    def clean(self) -> None:
        super().clean()
        if self.aci_aaep_id and self.aci_endpoint_group_id:
            # The EPG's tenant must live in the same fabric as the AAEP.
            aaep_fabric_id = self.aci_aaep.aci_fabric_id
            epg_fabric_id = self.aci_endpoint_group.aci_tenant.aci_fabric_id
            if aaep_fabric_id != epg_fabric_id:
                raise ValidationError(
                    {"aci_endpoint_group": _("The EPG must belong to the same Fabric as the AAEP.")}
                )

        if self.aci_aaep_id and self.encap_vlan is not None:
            # APIC will refuse to deploy an AAEP→EPG mapping whose encap
            # VLAN doesn't fall in the encap range of *any* VLAN pool
            # reachable through the AAEP's domain associations. We mirror
            # that constraint here so the user sees the problem at
            # configuration time, not when the leaves reject the policy.
            #
            # We only run the check when:
            #   * the AAEP has at least one domain attached, AND
            #   * at least one of those domains has a VLAN pool bound
            # otherwise the user is still building up policy and the
            # encap is allowed to sit unverified — same forgiving
            # behaviour APIC exhibits during incremental config.
            #
            # `ACIAAEPDomainAssociation` is the through model, so we
            # join on it explicitly to avoid the implicit M2M `through_fields`
            # lookup gymnastics.
            # Local import: `models/access/__init__.py` imports `aaeps`
            # before `vlan_pools`, so a top-level import here would force
            # vlan_pools to be evaluated while aaeps is still loading.
            # The local import sidesteps that and only fires when clean()
            # actually runs (well after the package is fully initialised).
            from netbox_cisco_aci.models.access.vlan_pools import (
                ACIVLANPoolBlock,
            )

            pool_ids = list(
                ACIAAEPDomainAssociation.objects.filter(aci_aaep_id=self.aci_aaep_id)
                .exclude(aci_domain__aci_vlan_pool__isnull=True)
                .values_list("aci_domain__aci_vlan_pool_id", flat=True)
                .distinct()
            )
            if pool_ids:
                covered = ACIVLANPoolBlock.objects.filter(
                    aci_vlan_pool_id__in=pool_ids,
                    from_vlan__lte=self.encap_vlan,
                    to_vlan__gte=self.encap_vlan,
                ).exists()
                if not covered:
                    raise ValidationError(
                        {
                            "encap_vlan": _(
                                "Encap VLAN %(vlan)d is not covered by any VLAN pool block "
                                "reachable through this AAEP's domains. Either expand a pool "
                                "or attach a domain whose pool includes this VLAN."
                            )
                            % {"vlan": self.encap_vlan},
                        }
                    )
