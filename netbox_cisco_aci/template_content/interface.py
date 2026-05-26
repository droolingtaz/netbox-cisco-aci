"""Interface detail page extension: ACI context panel."""

from netbox.plugins import PluginTemplateExtension

from ..models.bindings import ACIInterfaceFabricMembership, ACIStaticPortBinding
from ..models.contracts import ACIContractRelation


class ACIInterfaceContextPanel(PluginTemplateExtension):
    """Inject an ACI context panel into the dcim.Interface detail view."""

    models = ["dcim.interface"]

    def right_page(self):
        interface = self.context.get("object")
        if interface is None:
            return ""

        bindings = list(
            ACIStaticPortBinding.objects.filter(dcim_interface=interface).select_related(
                "aci_endpoint_group__aci_tenant",
                "aci_endpoint_group__aci_bridge_domain__aci_vrf",
                "aci_endpoint_group__aci_app_profile",
            )[:25]
        )

        membership = (
            ACIInterfaceFabricMembership.objects.select_related("aci_node")
            .filter(dcim_interface=interface)
            .first()
        )

        if not bindings and membership is None:
            return ""

        # Dedup BDs/Subnets/VRFs by id for display.
        seen_subnets: dict = {}
        for b in bindings:
            bd = b.aci_endpoint_group.aci_bridge_domain
            if bd is None:
                continue
            for subnet in bd.subnets.all():
                seen_subnets.setdefault(subnet.pk, subnet)
        subnets = list(seen_subnets.values())

        epg_ids = [b.aci_endpoint_group_id for b in bindings]
        if epg_ids:
            relations = ACIContractRelation.objects.filter(
                aci_endpoint_group_id__in=epg_ids
            ).select_related("aci_contract")
            provided_contracts = [r for r in relations if r.role == "provider"]
            consumed_contracts = [r for r in relations if r.role == "consumer"]
        else:
            provided_contracts = []
            consumed_contracts = []

        return self.render(
            "netbox_cisco_aci/inc/interface_aci_context.html",
            extra_context={
                "interface_fabric_membership": membership,
                "static_port_bindings": bindings,
                "subnets": subnets,
                "provided_contracts": provided_contracts,
                "consumed_contracts": consumed_contracts,
            },
        )
