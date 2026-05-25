"""Shared test fixtures for the plugin's test suite."""

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site


def make_dcim_device(name: str = "leaf-101") -> Device:
    """Build a throwaway dcim.Device for tests that need a linked node."""

    site, _ = Site.objects.get_or_create(name="ACI-Test-Site", slug="aci-test-site")
    manufacturer, _ = Manufacturer.objects.get_or_create(name="Cisco", slug="cisco")
    device_type, _ = DeviceType.objects.get_or_create(
        manufacturer=manufacturer, model="N9K-C9336C-FX2", slug="n9k-c9336c-fx2"
    )
    device_role, _ = DeviceRole.objects.get_or_create(name="ACI Leaf", slug="aci-leaf")
    return Device.objects.create(
        name=name, site=site, device_type=device_type, role=device_role
    )
