"""ACI Interface Fabric Membership — per-interface ACI Node attribution."""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import InterfaceFabricRoleChoices
from ..base import ACIBaseModel


class ACIInterfaceFabricMembership(ACIBaseModel):
    """Links a ``dcim.Interface`` to an ACI Node with a fabric role.

    The Device-level link (ACINode ↔ dcim.Device via GFK) already
    exists; this model adds the per-interface complement so visibility
    panels can resolve a NetBox interface to its ACI fabric without
    walking through the device.
    """

    dcim_interface = models.OneToOneField(
        to="dcim.Interface",
        on_delete=models.CASCADE,
        related_name="aci_fabric_membership",
        verbose_name=_("NetBox Interface"),
    )
    aci_node = models.ForeignKey(
        to="netbox_cisco_aci.ACINode",
        on_delete=models.CASCADE,
        related_name="interface_memberships",
        verbose_name=_("ACI Node"),
    )
    interface_role = models.CharField(
        verbose_name=_("Interface role"),
        max_length=16,
        default=InterfaceFabricRoleChoices.HOST,
        choices=InterfaceFabricRoleChoices,
    )

    clone_fields = ("aci_node", "interface_role")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Interface Fabric Membership")
        verbose_name_plural = _("ACI Interface Fabric Memberships")
        ordering = ("aci_node", "dcim_interface")

    def __str__(self) -> str:
        return f"{self.aci_node.name} / {self.dcim_interface}"

    def get_absolute_url(self) -> str:
        return reverse(
            "plugins:netbox_cisco_aci:aciinterfacefabricmembership",
            args=[self.pk],
        )

    def save(self, *args, **kwargs):
        if not self.name and self.aci_node_id and self.dcim_interface_id:
            node_name = getattr(self.aci_node, "name", "")
            iface_name = str(self.dcim_interface).replace("/", "_").replace(" ", "_")
            import re

            candidate = f"ifm_{node_name}_{iface_name}"
            candidate = re.sub(r"[^A-Za-z0-9._:\-]", "_", candidate)
            self.name = candidate[:64]
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if not (self.dcim_interface_id and self.aci_node_id):
            return

        node_ct_id = self.aci_node.node_object_type_id
        node_obj_id = self.aci_node.node_object_id
        if node_ct_id is None or node_obj_id is None:
            return

        try:
            ct = ContentType.objects.get_for_id(node_ct_id)
        except ContentType.DoesNotExist:  # pragma: no cover
            return

        if ct.app_label != "dcim" or ct.model != "device":
            # Node points at a VirtualMachine (or other) — physical interface
            # consistency does not apply.
            return

        iface_device_id = getattr(self.dcim_interface, "device_id", None)
        if iface_device_id is not None and iface_device_id != node_obj_id:
            raise ValidationError(
                {"dcim_interface": _("Interface's device must match the ACI Node's linked device.")}
            )
