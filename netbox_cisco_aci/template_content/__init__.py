"""PluginTemplateExtensions for core NetBox object detail pages.

These inject ACI-context panels into dcim.Device and dcim.Interface
detail views so an operator can see, at a glance, which EPGs, BDs,
subnets, and VRFs touch a piece of hardware.
"""

from .device import ACIDeviceContextPanel
from .interface import ACIInterfaceContextPanel

template_extensions = (
    ACIDeviceContextPanel,
    ACIInterfaceContextPanel,
)
