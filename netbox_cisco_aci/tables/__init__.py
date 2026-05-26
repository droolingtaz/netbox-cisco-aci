"""django-tables2 tables for the plugin."""

from .access import (  # noqa: F401
    ACIAAEPEPGMappingTable,
    ACIAAEPTable,
    ACIDomainTable,
    ACIVLANPoolBlockTable,
    ACIVLANPoolTable,
)
from .access_groups import ACIInterfacePolicyGroupTable  # noqa: F401
from .access_policies import (  # noqa: F401
    ACICDPInterfacePolicyTable,
    ACILACPInterfacePolicyTable,
    ACILinkLevelPolicyTable,
    ACILLDPInterfacePolicyTable,
    ACIMCPInterfacePolicyTable,
    ACISTPInterfacePolicyTable,
)
from .access_profiles import (  # noqa: F401
    ACIInterfaceProfileSelectorTable,
    ACIInterfaceProfileTable,
    ACISwitchProfileInterfaceProfileAttachmentTable,
    ACISwitchProfileSelectorTable,
    ACISwitchProfileTable,
)
from .fabric import ACIFabricTable, ACINodeTable, ACIPodTable  # noqa: F401
from .tenant import (  # noqa: F401
    ACIAppProfileTable,
    ACIBridgeDomainSubnetTable,
    ACIBridgeDomainTable,
    ACIEndpointGroupTable,
    ACIEndpointSecurityGroupTable,
    ACITenantTable,
    ACIUSegAttributeTable,
    ACIVRFTable,
)
