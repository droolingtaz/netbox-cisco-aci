"""Top-level NetBox navigation entries for the plugin."""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem


def _item(link: str, text: str) -> PluginMenuItem:
    return PluginMenuItem(
        link=f"plugins:netbox_cisco_aci:{link}_list",
        link_text=text,
        buttons=(
            PluginMenuButton(
                link=f"plugins:netbox_cisco_aci:{link}_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    )


fabric_items = (
    _item("acifabric", "Fabrics"),
    _item("acipod", "Pods"),
    _item("acinode", "Nodes"),
)

access_items = (
    _item("acivlanpool", "VLAN Pools"),
    _item("acivlanpoolblock", "VLAN Pool Blocks"),
    _item("acidomain", "Domains"),
    _item("aciaaep", "AAEPs"),
    _item("aciaaepepgmapping", "AAEP → EPG Mappings"),
)

interface_policy_items = (
    _item("acilinklevelpolicy", "Link Level"),
    _item("acicdpinterfacepolicy", "CDP"),
    _item("acilldpinterfacepolicy", "LLDP"),
    _item("acilacpinterfacepolicy", "LACP"),
    _item("acimcpinterfacepolicy", "MCP"),
    _item("acistpinterfacepolicy", "STP"),
    _item("aciinterfacepolicygroup", "Policy Groups"),
)

access_profile_items = (
    _item("aciswitchprofile", "Switch Profiles"),
    _item("aciswitchprofileselector", "Switch Profile Selectors"),
    _item("aciinterfaceprofile", "Interface Profiles"),
    _item("aciinterfaceprofileselector", "Interface Profile Selectors"),
    _item("aciswitchprofileinterfaceprofileattachment", "Switch ↔ Interface Attachments"),
)

contract_items = (
    _item("acicontract", "Contracts"),
    _item("acisubject", "Subjects"),
    _item("acisubjectfilter", "Subject Filters"),
    _item("acifilter", "Filters"),
    _item("acifilterentry", "Filter Entries"),
    _item("acicontractrelation", "Contract Relations"),
)

binding_items = (
    _item("acistaticportbinding", "Static Port Bindings"),
    _item("acivpcbindingpair", "vPC Binding Pairs"),
    _item("acidomainbinding", "Domain Bindings"),
    _item("aciinterfacefabricmembership", "Interface Fabric Memberships"),
)

tenancy_items = (
    _item("acitenant", "Tenants"),
    _item("acivrf", "VRFs"),
    _item("acibridgedomain", "Bridge Domains"),
    _item("acibridgedomainsubnet", "BD Subnets"),
    _item("aciappprofile", "Application Profiles"),
    _item("aciendpointgroup", "Endpoint Groups"),
    _item("aciusegattribute", "uSeg Attributes"),
    _item("aciendpointsecuritygroup", "Endpoint Security Groups"),
)

menu = PluginMenu(
    label="Cisco ACI",
    groups=(
        ("Fabric", fabric_items),
        ("Tenancy", tenancy_items),
        ("Access Policies", access_items),
        ("Interface Policies", interface_policy_items),
        ("Access Profiles", access_profile_items),
        ("Contracts", contract_items),
        ("Static Port Bindings", binding_items),
        # Subsequent phases extend this tuple — L3Outs.
    ),
    icon_class="mdi mdi-server-network",
)
