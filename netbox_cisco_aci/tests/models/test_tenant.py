"""Model-level tests for Phase 2: Tenancy."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIBridgeDomainSubnet,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
    ACIUSegAttribute,
)


class _TenancyFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fabric = ACIFabric.objects.create(name="DC1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fabric, name="acme")
        cls.common = ACITenant.objects.create(aci_fabric=cls.fabric, name="common")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.common_vrf = ACIVRF.objects.create(aci_tenant=cls.common, name="vrf-shared")
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-web")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-web"
        )


class ACITenantTests(_TenancyFixture):
    def test_unique_name_inside_fabric(self):
        with self.assertRaises(IntegrityError):
            ACITenant.objects.create(aci_fabric=self.fabric, name="acme")

    def test_same_name_in_different_fabric(self):
        other_fab = ACIFabric.objects.create(name="DC2")
        ACITenant.objects.create(aci_fabric=other_fab, name="acme")  # no raise


class ACIVRFTests(_TenancyFixture):
    def test_default_enforcement_is_enforced_ingress(self):
        v = ACIVRF.objects.create(aci_tenant=self.tenant, name="vrf-x")
        self.assertEqual(v.policy_enforcement_preference, "enforced")
        self.assertEqual(v.policy_enforcement_direction, "ingress")

    def test_unique_inside_tenant(self):
        with self.assertRaises(IntegrityError):
            ACIVRF.objects.create(aci_tenant=self.tenant, name="vrf-prod")


class ACIBridgeDomainTests(_TenancyFixture):
    def test_bd_in_same_tenant_passes_clean(self):
        ACIBridgeDomain(aci_tenant=self.tenant, aci_vrf=self.vrf, name="bd-clean").full_clean()

    def test_bd_with_common_tenant_vrf_passes_clean(self):
        bd = ACIBridgeDomain(aci_tenant=self.tenant, aci_vrf=self.common_vrf, name="bd-via-common")
        bd.full_clean()

    def test_bd_with_foreign_vrf_fails_clean(self):
        other_tenant = ACITenant.objects.create(aci_fabric=self.fabric, name="other")
        other_vrf = ACIVRF.objects.create(aci_tenant=other_tenant, name="vrf-other")
        bd = ACIBridgeDomain(aci_tenant=self.tenant, aci_vrf=other_vrf, name="bd-foreign")
        with self.assertRaises(ValidationError):
            bd.full_clean()


class ACIBridgeDomainSubnetTests(_TenancyFixture):
    def test_unique_gateway_inside_bd(self):
        ACIBridgeDomainSubnet.objects.create(
            aci_bridge_domain=self.bd, name="primary", gateway_ip="10.0.0.1/24"
        )
        with self.assertRaises(IntegrityError):
            ACIBridgeDomainSubnet.objects.create(
                aci_bridge_domain=self.bd, name="dup", gateway_ip="10.0.0.1/24"
            )


class ACIEndpointGroupTests(_TenancyFixture):
    def test_ap_tenant_mismatch_rejected(self):
        other_tenant = ACITenant.objects.create(aci_fabric=self.fabric, name="t2")
        other_ap = ACIAppProfile.objects.create(aci_tenant=other_tenant, name="ap-x")
        epg = ACIEndpointGroup(
            aci_tenant=self.tenant,
            aci_app_profile=other_ap,
            aci_bridge_domain=self.bd,
            name="epg-bad",
        )
        with self.assertRaises(ValidationError):
            epg.full_clean()

    def test_bd_in_common_allowed(self):
        common_bd = ACIBridgeDomain.objects.create(
            aci_tenant=self.common, aci_vrf=self.common_vrf, name="bd-common"
        )
        epg = ACIEndpointGroup(
            aci_tenant=self.tenant,
            aci_app_profile=self.ap,
            aci_bridge_domain=common_bd,
            name="epg-common",
        )
        epg.full_clean()

    def test_unique_inside_ap(self):
        ACIEndpointGroup.objects.create(
            aci_tenant=self.tenant,
            aci_app_profile=self.ap,
            aci_bridge_domain=self.bd,
            name="epg-a",
        )
        with self.assertRaises(IntegrityError):
            ACIEndpointGroup.objects.create(
                aci_tenant=self.tenant,
                aci_app_profile=self.ap,
                aci_bridge_domain=self.bd,
                name="epg-a",
            )


class ACIUSegAttributeTests(_TenancyFixture):
    def test_useg_attr_requires_useg_epg(self):
        regular_epg = ACIEndpointGroup.objects.create(
            aci_tenant=self.tenant,
            aci_app_profile=self.ap,
            aci_bridge_domain=self.bd,
            name="epg-regular",
        )
        attr = ACIUSegAttribute(
            aci_endpoint_group=regular_epg,
            name="ip-rule",
            attribute_type="ip",
            match_value="10.0.0.0/24",
        )
        with self.assertRaises(ValidationError):
            attr.full_clean()

    def test_useg_attr_attaches_to_useg_epg(self):
        useg_epg = ACIEndpointGroup.objects.create(
            aci_tenant=self.tenant,
            aci_app_profile=self.ap,
            aci_bridge_domain=self.bd,
            name="epg-useg",
            is_useg=True,
        )
        ACIUSegAttribute(
            aci_endpoint_group=useg_epg,
            name="ip-rule",
            attribute_type="ip",
            match_value="10.0.0.0/24",
        ).full_clean()


class ACIEndpointSecurityGroupTests(_TenancyFixture):
    def test_vrf_must_match_tenant(self):
        other_tenant = ACITenant.objects.create(aci_fabric=self.fabric, name="t2")
        other_vrf = ACIVRF.objects.create(aci_tenant=other_tenant, name="vrf-x")
        esg = ACIEndpointSecurityGroup(aci_tenant=self.tenant, aci_vrf=other_vrf, name="esg-bad")
        with self.assertRaises(ValidationError):
            esg.full_clean()

    def test_unique_inside_vrf(self):
        ACIEndpointSecurityGroup.objects.create(
            aci_tenant=self.tenant, aci_vrf=self.vrf, name="esg-a"
        )
        with self.assertRaises(IntegrityError):
            ACIEndpointSecurityGroup.objects.create(
                aci_tenant=self.tenant, aci_vrf=self.vrf, name="esg-a"
            )
