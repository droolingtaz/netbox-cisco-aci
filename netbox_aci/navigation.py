"""Top-level NetBox navigation entries for the plugin."""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem


def _item(link: str, text: str) -> PluginMenuItem:
    return PluginMenuItem(
        link=f"plugins:netbox_aci:{link}_list",
        link_text=text,
        buttons=(
            PluginMenuButton(
                link=f"plugins:netbox_aci:{link}_add",
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
        # Subsequent phases extend this tuple — Access policies,
        # Contracts, L3Outs, Static Port Bindings.
    ),
    icon_class="mdi mdi-server-network",
)
