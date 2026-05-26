"""ACI vPC Binding Pair — groups two leaf-side static port bindings.

APIC expresses a vPC binding as a single attachment to a vPC name path;
in NetBox we keep the two physical interface bindings explicit so the
Device / Interface visibility panels resolve cleanly on both peers.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import StaticPortBindingTypeChoices
from ..base import ACIBaseModel


class ACIVPCBindingPair(ACIBaseModel):
    """Pair of :class:`ACIStaticPortBinding`s forming a single vPC."""

    binding_a = models.OneToOneField(
        to="netbox_cisco_aci.ACIStaticPortBinding",
        on_delete=models.CASCADE,
        related_name="vpc_pair_as_a",
        verbose_name=_("Binding A"),
    )
    binding_b = models.OneToOneField(
        to="netbox_cisco_aci.ACIStaticPortBinding",
        on_delete=models.CASCADE,
        related_name="vpc_pair_as_b",
        verbose_name=_("Binding B"),
    )

    clone_fields = ("binding_a", "binding_b", "description")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI vPC Binding Pair")
        verbose_name_plural = _("ACI vPC Binding Pairs")
        ordering = ("binding_a",)
        constraints = (
            models.UniqueConstraint(
                fields=("binding_a",),
                name="netbox_cisco_aci_acivpcbindingpair_a_unique",
            ),
            models.CheckConstraint(
                condition=~Q(binding_a=F("binding_b")),
                name="netbox_cisco_aci_acivpcbindingpair_distinct",
            ),
        )

    def __str__(self) -> str:
        return f"vPC: {self.binding_a} <-> {self.binding_b}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acivpcbindingpair", args=[self.pk])

    def save(self, *args, **kwargs):
        if not self.name and self.binding_a_id and self.binding_b_id:
            self.name = f"vpc_pair_{self.binding_a_id}_{self.binding_b_id}"[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()

        if not (self.binding_a_id and self.binding_b_id):
            return

        if self.binding_a_id == self.binding_b_id:
            raise ValidationError(
                {"binding_b": _("vPC pair must reference two distinct bindings.")}
            )

        a, b = self.binding_a, self.binding_b

        if (
            a.binding_type != StaticPortBindingTypeChoices.VPC
            or b.binding_type != StaticPortBindingTypeChoices.VPC
        ):
            raise ValidationError(_("Both bindings in a vPC pair must have binding_type='vpc'."))

        if a.aci_endpoint_group_id != b.aci_endpoint_group_id:
            raise ValidationError(_("Both bindings in a vPC pair must reference the same EPG."))

        if a.encap_vlan != b.encap_vlan:
            raise ValidationError(_("Both bindings in a vPC pair must use the same encap VLAN."))

        a_device_id = getattr(a.dcim_interface, "device_id", None)
        b_device_id = getattr(b.dcim_interface, "device_id", None)
        if a_device_id is not None and a_device_id == b_device_id:
            raise ValidationError(
                _(
                    "vPC peer interfaces must live on different devices "
                    "(two leaves of the vPC pair)."
                )
            )

        # Cross-fabric guard: the two leaves must belong to the same fabric.
        from .fabric_membership import ACIInterfaceFabricMembership

        memberships = {
            m.dcim_interface_id: m
            for m in ACIInterfaceFabricMembership.objects.filter(
                dcim_interface_id__in=(a.dcim_interface_id, b.dcim_interface_id)
            ).select_related("aci_node__aci_pod__aci_fabric")
        }
        m_a = memberships.get(a.dcim_interface_id)
        m_b = memberships.get(b.dcim_interface_id)
        if m_a is not None and m_b is not None:
            fab_a = m_a.aci_node.aci_pod.aci_fabric_id
            fab_b = m_b.aci_node.aci_pod.aci_fabric_id
            if fab_a != fab_b:
                raise ValidationError(
                    _("vPC peer interfaces must belong to ACI Nodes in the same fabric.")
                )
