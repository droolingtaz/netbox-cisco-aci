"""Top-level NetBox navigation entries for the plugin."""

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

fabric_items = (
    PluginMenuItem(
        link="plugins:netbox_aci:acifabric_list",
        link_text="Fabrics",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_aci:acifabric_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_aci:acipod_list",
        link_text="Pods",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_aci:acipod_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_aci:acinode_list",
        link_text="Nodes",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_aci:acinode_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            ),
        ),
    ),
)

menu = PluginMenu(
    label="Cisco ACI",
    groups=(
        ("Fabric", fabric_items),
        # Subsequent phases extend this tuple — Tenancy, Access policies,
        # Contracts, L3Outs, Static Port Bindings — so the menu groups
        # stay aligned with the model packages on disk.
    ),
    icon_class="mdi mdi-server-network",
)
