"""Model-level tests for Phase 3: VLAN Pools, Domains, AAEPs."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import (
    DomainTypeChoices,
    StaticPortModeChoices,
    VLANPoolAllocationChoices,
)
from netbox_cisco_aci.models.access import (
    ACIAAEP,
    ACIAAEPDomainAssociation,
    ACIAAEPEPGMapping,
    ACIDomain,
    ACIVLANPool,
    ACIVLANPoolBlock,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACITenant,
)


class _AccessFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.fab2 = ACIFabric.objects.create(name="DC2")
        cls.pool = ACIVLANPool.objects.create(
            aci_fabric=cls.fab,
            name="pool-prod",
            allocation_mode=VLANPoolAllocationChoices.STATIC,
        )
        cls.domain = ACIDomain.objects.create(
            aci_fabric=cls.fab,
            name="phys-prod",
            domain_type=DomainTypeChoices.PHYSICAL,
            aci_vlan_pool=cls.pool,
        )
        cls.aaep = ACIAAEP.objects.create(aci_fabric=cls.fab, name="aaep-prod")

        # Bare tenant + EPG so the EPG-mapping tests have a target.
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.vrf = ACIVRF.objects.create(aci_tenant=cls.tenant, name="vrf-prod")
        cls.ap = ACIAppProfile.objects.create(aci_tenant=cls.tenant, name="ap-web")
        cls.bd = ACIBridgeDomain.objects.create(
            aci_tenant=cls.tenant, aci_vrf=cls.vrf, name="bd-web"
        )
        cls.epg = ACIEndpointGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_app_profile=cls.ap,
            aci_bridge_domain=cls.bd,
            name="epg-web",
        )


class ACIVLANPoolTests(_AccessFixture):
    def test_unique_inside_fabric(self):
        with self.assertRaises(IntegrityError):
            ACIVLANPool.objects.create(aci_fabric=self.fab, name="pool-prod")

    def test_same_name_in_different_fabric(self):
        ACIVLANPool.objects.create(aci_fabric=self.fab2, name="pool-prod")


class ACIVLANPoolBlockTests(_AccessFixture):
    def test_to_must_be_ge_from(self):
        b = ACIVLANPoolBlock(aci_vlan_pool=self.pool, name="b", from_vlan=100, to_vlan=50)
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_no_overlap_inside_same_pool(self):
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="a", from_vlan=100, to_vlan=200
        )
        b = ACIVLANPoolBlock(aci_vlan_pool=self.pool, name="b", from_vlan=150, to_vlan=250)
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_overlap_allowed_across_pools(self):
        other_pool = ACIVLANPool.objects.create(aci_fabric=self.fab, name="pool-other")
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="a", from_vlan=100, to_vlan=200
        )
        b = ACIVLANPoolBlock(aci_vlan_pool=other_pool, name="b", from_vlan=150, to_vlan=250)
        b.full_clean()
        b.save()


class ACIDomainTests(_AccessFixture):
    def test_unique_inside_fabric(self):
        with self.assertRaises(IntegrityError):
            ACIDomain.objects.create(
                aci_fabric=self.fab,
                name="phys-prod",
                domain_type=DomainTypeChoices.PHYSICAL,
            )

    def test_domain_type_color_lookup(self):
        self.assertEqual(self.domain.get_domain_type_color(), "blue")


class ACIAAEPDomainAssociationTests(_AccessFixture):
    def test_associate_same_fabric(self):
        assoc = ACIAAEPDomainAssociation(aci_aaep=self.aaep, aci_domain=self.domain)
        assoc.full_clean()
        assoc.save()

    def test_reject_cross_fabric_association(self):
        # Domain in DC2; AAEP in DC1 -> cross-fabric, must fail.
        foreign_pool = ACIVLANPool.objects.create(aci_fabric=self.fab2, name="pool-x")
        foreign_dom = ACIDomain.objects.create(
            aci_fabric=self.fab2,
            name="phys-x",
            domain_type=DomainTypeChoices.PHYSICAL,
            aci_vlan_pool=foreign_pool,
        )
        assoc = ACIAAEPDomainAssociation(aci_aaep=self.aaep, aci_domain=foreign_dom)
        with self.assertRaises(ValidationError):
            assoc.full_clean()


class ACIAAEPEPGMappingTests(_AccessFixture):
    def test_basic_mapping(self):
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m1",
            encap_vlan=200,
            mode=StaticPortModeChoices.TRUNK,
        )
        m.full_clean()
        m.save()

    def test_reject_cross_fabric_epg(self):
        other_tenant = ACITenant.objects.create(aci_fabric=self.fab2, name="acme2")
        other_vrf = ACIVRF.objects.create(aci_tenant=other_tenant, name="vrf-x")
        other_ap = ACIAppProfile.objects.create(aci_tenant=other_tenant, name="ap-x")
        other_bd = ACIBridgeDomain.objects.create(
            aci_tenant=other_tenant, aci_vrf=other_vrf, name="bd-x"
        )
        other_epg = ACIEndpointGroup.objects.create(
            aci_tenant=other_tenant,
            aci_app_profile=other_ap,
            aci_bridge_domain=other_bd,
            name="epg-x",
        )
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=other_epg,
            name="m-bad",
            encap_vlan=200,
        )
        with self.assertRaises(ValidationError):
            m.full_clean()

    def test_unique_constraint(self):
        ACIAAEPEPGMapping.objects.create(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m1",
            encap_vlan=200,
        )
        with self.assertRaises(IntegrityError):
            ACIAAEPEPGMapping.objects.create(
                aci_aaep=self.aaep,
                aci_endpoint_group=self.epg,
                name="m1-dup",
                encap_vlan=200,
            )


# ---------------------------------------------------------------------------
# Extra coverage (Bucket B) — get_absolute_url + missed validation paths
# ---------------------------------------------------------------------------


class ACIVLANPoolBlockExtraTests(_AccessFixture):
    """Cover missed lines L50, 53, 106-108, 111, 115, 135 in vlan_pools.py."""

    def test_from_greater_than_to_raises_validation_error_with_message(self):
        b = ACIVLANPoolBlock(aci_vlan_pool=self.pool, name="bad-range", from_vlan=200, to_vlan=100)
        with self.assertRaisesRegex(ValidationError, "to_vlan"):
            b.full_clean()

    def test_overlap_error_message_contains_range(self):
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="base", from_vlan=500, to_vlan=600
        )
        b = ACIVLANPoolBlock(aci_vlan_pool=self.pool, name="overlap", from_vlan=550, to_vlan=650)
        with self.assertRaisesRegex(ValidationError, "550-650"):
            b.full_clean()

    def test_get_absolute_url_contains_pk(self):
        b = ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="url-test", from_vlan=700, to_vlan=800
        )
        self.assertIn(str(b.pk), b.get_absolute_url())

    def test_str_same_vlan(self):
        b = ACIVLANPoolBlock(aci_vlan_pool=self.pool, from_vlan=10, to_vlan=10)
        self.assertIn("VLAN 10", str(b))
        self.assertNotIn("10-10", str(b))


class ACIDomainExtraTests(_AccessFixture):
    """Cover get_absolute_url (L64 in domains.py)."""

    def test_get_absolute_url(self):
        self.assertIn(str(self.domain.pk), self.domain.get_absolute_url())


class ACIAAEPDomainAssociationExtraTests(_AccessFixture):
    """Cover missed lines L63, 66, 97 in aaeps.py."""

    def test_cross_fabric_error_message_mentions_fabric(self):
        foreign_pool = ACIVLANPool.objects.create(aci_fabric=self.fab2, name="pool-fab2-extra")
        foreign_dom = ACIDomain.objects.create(
            aci_fabric=self.fab2,
            name="phys-extra",
            domain_type=DomainTypeChoices.PHYSICAL,
            aci_vlan_pool=foreign_pool,
        )
        assoc = ACIAAEPDomainAssociation(aci_aaep=self.aaep, aci_domain=foreign_dom)
        with self.assertRaisesRegex(ValidationError, "Fabric"):
            assoc.full_clean()


class ACIAAEPEPGMappingExtraTests(_AccessFixture):
    """Cover missed lines L161, 167, 171 in aaeps.py."""

    def test_cross_fabric_epg_error_message_mentions_fabric(self):
        other_tenant = ACITenant.objects.create(aci_fabric=self.fab2, name="acme2-extra")
        other_vrf = ACIVRF.objects.create(aci_tenant=other_tenant, name="vrf-extra")
        other_ap = ACIAppProfile.objects.create(aci_tenant=other_tenant, name="ap-extra")
        other_bd = ACIBridgeDomain.objects.create(
            aci_tenant=other_tenant, aci_vrf=other_vrf, name="bd-extra"
        )
        other_epg = ACIEndpointGroup.objects.create(
            aci_tenant=other_tenant,
            aci_app_profile=other_ap,
            aci_bridge_domain=other_bd,
            name="epg-extra",
        )
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=other_epg,
            name="m-bad-extra",
            encap_vlan=300,
        )
        with self.assertRaisesRegex(ValidationError, "Fabric"):
            m.full_clean()

    def test_get_absolute_url(self):
        m = ACIAAEPEPGMapping.objects.create(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-url-test",
            encap_vlan=400,
        )
        self.assertIn(str(m.pk), m.get_absolute_url())


class ACIAAEPEPGMappingEncapPoolValidationTests(_AccessFixture):
    """Verify the encap VLAN must fall in a pool reachable through the AAEP.

    Mirrors APIC's behaviour: the leaves refuse to deploy an EPG mapping
    whose encap doesn't fall in the encap range of *any* VLAN pool
    bound to a domain attached to the AAEP. The plugin's clean() catches
    that at config time so the user doesn't ship an unreachable mapping.

    The check is intentionally permissive while the AAEP is still
    being built (no domains yet, or domains without pools), to mirror
    APIC's incremental-config tolerance.
    """

    def _associate_domain_with_pool_block(self, lo, hi):
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="blk-1", from_vlan=lo, to_vlan=hi
        )
        ACIAAEPDomainAssociation.objects.create(aci_aaep=self.aaep, aci_domain=self.domain)

    def test_skipped_when_aaep_has_no_domains(self):
        # AAEP has zero domain attachments; encap is permitted.
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-no-domains",
            encap_vlan=200,
        )
        m.full_clean()  # no-raise = passes

    def test_skipped_when_attached_domain_has_no_pool(self):
        # Strip the pool off the seeded domain so the AAEP has a domain
        # but no reachable pool. Encap is still permitted.
        self.domain.aci_vlan_pool = None
        self.domain.save()
        ACIAAEPDomainAssociation.objects.create(aci_aaep=self.aaep, aci_domain=self.domain)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-pool-less",
            encap_vlan=200,
        )
        m.full_clean()

    def test_encap_inside_pool_block_allowed(self):
        self._associate_domain_with_pool_block(100, 200)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-in-range",
            encap_vlan=150,
        )
        m.full_clean()

    def test_encap_at_pool_block_lower_bound_allowed(self):
        self._associate_domain_with_pool_block(100, 200)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-low",
            encap_vlan=100,
        )
        m.full_clean()

    def test_encap_at_pool_block_upper_bound_allowed(self):
        self._associate_domain_with_pool_block(100, 200)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-high",
            encap_vlan=200,
        )
        m.full_clean()

    def test_encap_outside_all_pool_blocks_rejected(self):
        self._associate_domain_with_pool_block(100, 200)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-out-of-range",
            encap_vlan=500,
        )
        with self.assertRaisesRegex(ValidationError, "VLAN pool block"):
            m.full_clean()

    def test_encap_covered_by_one_of_several_pool_blocks(self):
        # Multiple non-contiguous blocks under the same pool. Picking an
        # encap inside the second block must be allowed.
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="blk-low", from_vlan=100, to_vlan=199
        )
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="blk-high", from_vlan=300, to_vlan=399
        )
        ACIAAEPDomainAssociation.objects.create(aci_aaep=self.aaep, aci_domain=self.domain)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-second-block",
            encap_vlan=350,
        )
        m.full_clean()

    def test_encap_covered_by_pool_on_other_attached_domain(self):
        # AAEP has two domains; only the second one's pool covers the encap.
        # The mapping should still be allowed.
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=self.pool, name="blk-narrow", from_vlan=100, to_vlan=110
        )
        ACIAAEPDomainAssociation.objects.create(aci_aaep=self.aaep, aci_domain=self.domain)
        # second pool / domain whose range covers the encap
        wide_pool = ACIVLANPool.objects.create(
            aci_fabric=self.fab,
            name="pool-wide",
            allocation_mode=VLANPoolAllocationChoices.STATIC,
        )
        ACIVLANPoolBlock.objects.create(
            aci_vlan_pool=wide_pool, name="blk-wide", from_vlan=400, to_vlan=500
        )
        wide_dom = ACIDomain.objects.create(
            aci_fabric=self.fab,
            name="phys-wide",
            domain_type=DomainTypeChoices.PHYSICAL,
            aci_vlan_pool=wide_pool,
        )
        ACIAAEPDomainAssociation.objects.create(aci_aaep=self.aaep, aci_domain=wide_dom)
        m = ACIAAEPEPGMapping(
            aci_aaep=self.aaep,
            aci_endpoint_group=self.epg,
            name="m-wide-domain",
            encap_vlan=450,
        )
        m.full_clean()
