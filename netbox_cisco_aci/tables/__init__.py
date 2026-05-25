"""django-tables2 tables for the plugin."""

from .access import (  # noqa: F401
    ACIAAEPEPGMappingTable,
    ACIAAEPTable,
    ACIDomainTable,
    ACIVLANPoolBlockTable,
    ACIVLANPoolTable,
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
