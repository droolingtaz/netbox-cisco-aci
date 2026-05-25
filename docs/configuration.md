# Configuration

The plugin works with sensible defaults. The following settings live
under `PLUGINS_CONFIG['netbox_aci']` in `configuration.py`:

| Setting                          | Default | Purpose |
|----------------------------------|---------|---------|
| `default_node_id_min`            | `1`     | Lower bound for ACI node IDs (Cisco ships fabrics that start at 101 for spines, 200+ for leaves — this is just the validator floor). |
| `default_node_id_max`            | `4000`  | Upper bound for ACI node IDs. |
| `interface_panel_max_rows`       | `25`    | Caps the number of EPG rows rendered in the per-interface ACI panel. |
| `device_panel_max_rows`          | `100`   | Caps the number of EPG rows rendered in the per-device ACI panel. |
| `enable_template_extensions`     | `true`  | Master switch for the Device / Interface template extensions. |

All settings are optional. Unset values fall back to the defaults
above.
