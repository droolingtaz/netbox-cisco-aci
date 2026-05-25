"""ACI Node — a switch or controller inside a Pod."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import NodeRoleChoices, NodeTypeChoices
from ...constants import NODE_ID_MAX, NODE_ID_MIN, NODE_OBJECT_TYPES
from ..base import ACIFabricBaseModel


class ACINode(ACIFabricBaseModel):
    """An ACI Node (spine, leaf, APIC, remote leaf, virtual leaf).

    Each Node may optionally point at an existing ``dcim.Device`` or
    ``virtualization.VirtualMachine`` so NetBox remains the source of
    truth for hardware. The link is a GenericForeignKey so the user is
    not forced into a particular layout — physical leaves typically
    point at ``dcim.Device`` while virtual leaves point at a VM.
    """

    aci_pod = models.ForeignKey(
        to="netbox_aci.ACIPod",
        on_delete=models.PROTECT,
        related_name="nodes",
        verbose_name=_("ACI Pod"),
    )
    node_id = models.PositiveSmallIntegerField(
        verbose_name=_("Node ID"),
        validators=[MinValueValidator(NODE_ID_MIN), MaxValueValidator(NODE_ID_MAX)],
        help_text=_(
            "Node ID as assigned on the APIC. Cisco convention reserves 101-199 "
            "for spines and 200+ for leaves; the plugin does not enforce that "
            "split but the Best-Practice audit will flag deviations."
        ),
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=16,
        default=NodeRoleChoices.ROLE_LEAF,
        choices=NodeRoleChoices,
    )
    node_type = models.CharField(
        verbose_name=_("Type"),
        max_length=16,
        default=NodeTypeChoices.TYPE_PHYSICAL,
        choices=NodeTypeChoices,
    )
    serial_number = models.CharField(
        verbose_name=_("Serial number"),
        max_length=64,
        blank=True,
        help_text=_("Switch serial as reported by APIC (fabricNode.serial)."),
    )
    pod_tep_pool = models.CharField(
        verbose_name=_("Pod TEP pool"),
        max_length=64,
        blank=True,
        help_text=_("Pod TEP pool the node is part of (e.g. 10.0.0.0/16)."),
    )
    firmware_version = models.CharField(
        verbose_name=_("Firmware version"),
        max_length=64,
        blank=True,
    )

    # Generic link to dcim.Device / virtualization.VirtualMachine.
    node_object_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.PROTECT,
        related_name="+",
        limit_choices_to=NODE_OBJECT_TYPES,
        verbose_name=_("Node object type"),
        blank=True,
        null=True,
    )
    node_object_id = models.PositiveBigIntegerField(
        verbose_name=_("Node object ID"),
        blank=True,
        null=True,
    )
    node_object = GenericForeignKey(
        ct_field="node_object_type",
        fk_field="node_object_id",
    )

    clone_fields = ("aci_pod", "role", "node_type", "pod_tep_pool")

    class Meta(ACIFabricBaseModel.Meta):
        verbose_name = _("ACI Node")
        verbose_name_plural = _("ACI Nodes")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_pod", "node_id"),
                name="netbox_aci_acinode_pod_nodeid_unique",
            ),
            models.UniqueConstraint(
                fields=("aci_pod", "name"),
                name="netbox_aci_acinode_pod_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_pod} / Node {self.node_id} ({self.name})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_aci:acinode", args=[self.pk])

    def clean(self) -> None:
        super().clean()
        # GFK consistency: both columns or neither.
        if (self.node_object_type_id is None) != (self.node_object_id is None):
            raise ValidationError(
                _("node_object_type and node_object_id must be set together, or both left blank.")
            )

    @property
    def aci_fabric(self):
        """Convenience accessor — Fabric this node lives in."""
        return self.aci_pod.aci_fabric

    def get_role_color(self) -> str:
        return NodeRoleChoices.colors.get(self.role, "gray")

    def get_node_type_color(self) -> str:
        return NodeTypeChoices.colors.get(self.node_type, "gray")
