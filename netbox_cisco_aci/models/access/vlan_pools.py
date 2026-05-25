"""ACI VLAN Pools and their encap blocks."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import VLANPoolAllocationChoices
from ...constants import VLAN_ID_MAX, VLAN_ID_MIN
from ..base import ACIFabricBaseModel


class ACIVLANPool(ACIFabricBaseModel):
    """An ACI VLAN Pool (``fvnsVlanInstP``).

    Pools are fabric-scoped and contain one or more :class:`ACIVLANPoolBlock`
    children, each carving out a VLAN-ID range. A pool's ``allocation_mode``
    must match the encap-block roles assigned to its consumers (physical
    domains -> static, VMM domains -> dynamic, etc.). The model does not
    enforce that pairing; the Best-Practice audit will flag mismatches.
    """

    aci_fabric = models.ForeignKey(
        to="netbox_cisco_aci.ACIFabric",
        on_delete=models.PROTECT,
        related_name="vlan_pools",
        verbose_name=_("ACI Fabric"),
    )
    allocation_mode = models.CharField(
        verbose_name=_("Allocation mode"),
        max_length=16,
        default=VLANPoolAllocationChoices.STATIC,
        choices=VLANPoolAllocationChoices,
    )

    clone_fields = ("aci_fabric", "allocation_mode", "description")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI VLAN Pool")
        verbose_name_plural = _("ACI VLAN Pools")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_fabric", "name"),
                name="netbox_cisco_aci_acivlanpool_fabric_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_fabric.name} / Pool {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acivlanpool", args=[self.pk])


class ACIVLANPoolBlock(ACIFabricBaseModel):
    """A VLAN-ID range inside an :class:`ACIVLANPool` (``fvnsEncapBlk``).

    Blocks may overlap *across* pools (the Best-Practice audit warns on
    pools that overlap and reach the same leaves), but cannot overlap
    inside the same pool. ``name`` is optional in APIC; we keep it for
    NetBox-side documentation. Pool-scoped uniqueness is enforced on
    ``(pool, from_vlan, to_vlan)`` rather than on ``name`` so an
    operator can re-use a blank label across pools.
    """

    aci_vlan_pool = models.ForeignKey(
        to="netbox_cisco_aci.ACIVLANPool",
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name=_("ACI VLAN Pool"),
    )
    from_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("From VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
    )
    to_vlan = models.PositiveSmallIntegerField(
        verbose_name=_("To VLAN"),
        validators=[MinValueValidator(VLAN_ID_MIN), MaxValueValidator(VLAN_ID_MAX)],
    )
    allocation_mode_override = models.CharField(
        verbose_name=_("Allocation mode override"),
        max_length=16,
        blank=True,
        choices=VLANPoolAllocationChoices,
        help_text=_(
            "Optional per-block override of the parent pool's allocation mode. "
            "Leave blank to inherit."
        ),
    )

    clone_fields = ("aci_vlan_pool", "allocation_mode_override")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI VLAN Pool Block")
        verbose_name_plural = _("ACI VLAN Pool Blocks")
        ordering = ("aci_vlan_pool", "from_vlan", "to_vlan")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_vlan_pool", "from_vlan", "to_vlan"),
                name="netbox_cisco_aci_acivlanpoolblock_pool_range_unique",
            ),
        )

    def __str__(self) -> str:
        if self.from_vlan == self.to_vlan:
            return f"{self.aci_vlan_pool} / VLAN {self.from_vlan}"
        return f"{self.aci_vlan_pool} / VLAN {self.from_vlan}-{self.to_vlan}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acivlanpoolblock", args=[self.pk])

    @property
    def aci_fabric(self):
        return self.aci_vlan_pool.aci_fabric

    def clean(self) -> None:
        super().clean()
        if (
            self.from_vlan is not None
            and self.to_vlan is not None
            and self.from_vlan > self.to_vlan
        ):
            raise ValidationError(
                {"to_vlan": _("`to_vlan` must be greater than or equal to `from_vlan`.")}
            )
        # No overlap with sibling blocks in the same pool.
        if self.aci_vlan_pool_id and self.from_vlan and self.to_vlan:
            qs = ACIVLANPoolBlock.objects.filter(
                aci_vlan_pool_id=self.aci_vlan_pool_id,
                from_vlan__lte=self.to_vlan,
                to_vlan__gte=self.from_vlan,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    _("VLAN range %(lo)d-%(hi)d overlaps another block in the same pool.")
                    % {"lo": self.from_vlan, "hi": self.to_vlan}
                )
