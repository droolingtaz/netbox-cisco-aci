"""Constants used across the plugin.

Anything that is a Cisco-documented range, a regex for an ACI naming
convention, or a `ContentType` limit-tuple lives here so the rest of
the code is free of magic numbers.
"""

from django.db.models import Q

# ---------------------------------------------------------------------------
# Naming
# ---------------------------------------------------------------------------

#: Max length of an ACI object name as enforced by APIC.
ACI_NAME_MAX_LEN = 64

#: Max length of an ACI alias.
ACI_ALIAS_MAX_LEN = 64

#: Max length of an ACI description.
ACI_DESCRIPTION_MAX_LEN = 128

#: Regex for ACI policy names — letters, digits, dash, underscore, dot.
#: Same constraint APIC enforces server-side.
ACI_POLICY_NAME_REGEX = r"^[A-Za-z0-9_.:-]+$"


# ---------------------------------------------------------------------------
# Fabric topology
# ---------------------------------------------------------------------------

#: Lowest legal ACI Node ID.
NODE_ID_MIN = 1

#: Highest legal ACI Node ID (Cisco-documented).
NODE_ID_MAX = 4000

#: ContentTypes a Node may be linked to. Stored as a Q so it can be passed
#: straight into ``limit_choices_to`` on a GenericForeignKey.
NODE_OBJECT_TYPES = (
    Q(app_label="dcim", model="device") | Q(app_label="virtualization", model="virtualmachine")
)


# ---------------------------------------------------------------------------
# VLANs / encaps
# ---------------------------------------------------------------------------

#: Lowest legal VLAN encap.
VLAN_ID_MIN = 1

#: Highest legal VLAN encap.
VLAN_ID_MAX = 4094

#: Default infra VLAN per ACI best practice.
DEFAULT_INFRA_VLAN = 3967


# ---------------------------------------------------------------------------
# Pod / Tenant
# ---------------------------------------------------------------------------

#: Lowest legal Pod ID.
POD_ID_MIN = 1

#: Highest legal Pod ID.
POD_ID_MAX = 254

#: The well-known shared "common" tenant. Used in scope-validation logic.
COMMON_TENANT_NAME = "common"

#: The well-known infrastructure tenant.
INFRA_TENANT_NAME = "infra"

#: The well-known management tenant.
MGMT_TENANT_NAME = "mgmt"

#: Tenants Cisco ships pre-configured. Surfaced in forms as read-only-ish.
RESERVED_TENANT_NAMES = (COMMON_TENANT_NAME, INFRA_TENANT_NAME, MGMT_TENANT_NAME)
