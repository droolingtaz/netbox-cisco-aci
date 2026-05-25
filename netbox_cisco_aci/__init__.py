"""netbox-cisco-aci — operational visibility for Cisco ACI inside NetBox."""

from netbox.plugins import PluginConfig

from .version import __version__


class NetBoxACIConfig(PluginConfig):
    """PluginConfig for netbox-cisco-aci.

    A single release supports both NetBox 4.5.x and 4.6.x. Bumping the
    upper bound is reserved for explicit compatibility-bump releases —
    feature PRs must not touch ``min_version`` or ``max_version``.
    """

    name = "netbox_cisco_aci"
    # Explicit ``label`` keeps Django and the NetBox plugin loader in
    # agreement — several reverse() lookups in tests (e.g. the API
    # namespace ``netbox_cisco_aci-api``) build their viewname from
    # ``app.label``.
    label = "netbox_cisco_aci"
    verbose_name = "Cisco ACI"
    description = (
        "Models Cisco ACI fabrics, tenants, EPGs, contracts, L3Outs, "
        "and per-interface bindings inside NetBox."
    )
    version = __version__
    author = "Blake Parker"
    author_email = "blake.parker@e280.com"
    base_url = "cisco-aci"

    min_version = "4.5.0"
    max_version = "4.6.99"

    required_settings: list[str] = []
    default_settings = {
        "default_node_id_min": 1,
        "default_node_id_max": 4000,
        "interface_panel_max_rows": 25,
        "device_panel_max_rows": 100,
        "enable_template_extensions": True,
    }


config = NetBoxACIConfig
