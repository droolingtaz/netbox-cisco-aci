"""Device detail page extension: ACI context panel."""

from django.contrib.contenttypes.models import ContentType
from netbox.plugins import PluginTemplateExtension

from ..models.bindings import ACIStaticPortBinding
from ..models.fabric import ACINode
from ..models.l3out import ACILogicalNode


class ACIDeviceContextPanel(PluginTemplateExtension):
    """Inject an ACI context panel into the dcim.Device detail view."""

    models = ["dcim.device"]

    def _resolve_node(self, device):
        """Return the ACINode whose GFK points at this device, or ``None``."""

        try:
            ct = ContentType.objects.get_for_model(device.__class__)
        except Exception:  # pragma: no cover - defensive
            return None
        return (
            ACINode.objects.select_related("aci_pod", "aci_pod__aci_fabric")
            .filter(node_object_type=ct, node_object_id=device.pk)
            .first()
        )

    def full_width_page(self):
        device = self.context.get("object")
        if device is None:
            return ""

        aci_node = self._resolve_node(device)
        logical_nodes = []
        if aci_node is not None:
            logical_nodes = list(
                ACILogicalNode.objects.filter(aci_node=aci_node)
                .select_related(
                    "aci_logical_node_profile",
                    "aci_logical_node_profile__aci_l3out",
                    "aci_logical_node_profile__aci_l3out__aci_tenant",
                )
                .order_by("aci_logical_node_profile__aci_l3out__name", "name")[:50]
            )
        bindings_qs = (
            ACIStaticPortBinding.objects.filter(dcim_interface__device_id=device.pk)
            .select_related(
                "aci_endpoint_group__aci_tenant",
                "aci_endpoint_group__aci_bridge_domain__aci_vrf",
                "dcim_interface",
            )
            .order_by("dcim_interface", "encap_vlan")
        )
        bindings = list(bindings_qs[:50])

        if aci_node is None and not bindings and not logical_nodes:
            return ""

        epg_ids = {b.aci_endpoint_group_id for b in bindings}
        bd_ids = {
            b.aci_endpoint_group.aci_bridge_domain_id
            for b in bindings
            if b.aci_endpoint_group.aci_bridge_domain_id
        }
        vrf_ids = {
            b.aci_endpoint_group.aci_bridge_domain.aci_vrf_id
            for b in bindings
            if b.aci_endpoint_group.aci_bridge_domain_id
            and b.aci_endpoint_group.aci_bridge_domain.aci_vrf_id
        }

        return self.render(
            "netbox_cisco_aci/inc/device_aci_context.html",
            extra_context={
                "aci_node": aci_node,
                "aci_fabric": aci_node.aci_fabric if aci_node else None,
                "aci_pod": aci_node.aci_pod if aci_node else None,
                "static_port_bindings": bindings,
                "epg_count": len(epg_ids),
                "bd_count": len(bd_ids),
                "vrf_count": len(vrf_ids),
                "binding_count": len(bindings),
                "logical_nodes": logical_nodes,
            },
        )
