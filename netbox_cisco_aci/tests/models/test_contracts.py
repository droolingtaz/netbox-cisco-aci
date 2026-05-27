"""Model-level tests for Phase 5: Contracts / Subjects / Filters / Relations."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from netbox_cisco_aci.choices import (
    ContractFilterEntryEtherTypeChoices,
    ContractFilterEntryIPProtocolChoices,
    ContractRelationRoleChoices,
    ContractScopeChoices,
    SubjectFilterActionChoices,
    SubjectFilterDirectionChoices,
)
from netbox_cisco_aci.constants import COMMON_TENANT_NAME
from netbox_cisco_aci.models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)
from netbox_cisco_aci.models.fabric import ACIFabric
from netbox_cisco_aci.models.tenant import (
    ACIVRF,
    ACIAppProfile,
    ACIBridgeDomain,
    ACIEndpointGroup,
    ACIEndpointSecurityGroup,
    ACITenant,
)


class _ContractFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fab = ACIFabric.objects.create(name="DC1")
        cls.tenant = ACITenant.objects.create(aci_fabric=cls.fab, name="acme")
        cls.tenant2 = ACITenant.objects.create(aci_fabric=cls.fab, name="other")
        cls.common = ACITenant.objects.create(aci_fabric=cls.fab, name=COMMON_TENANT_NAME)
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
        cls.esg = ACIEndpointSecurityGroup.objects.create(
            aci_tenant=cls.tenant,
            aci_vrf=cls.vrf,
            name="esg-web",
        )


# ---------------------------------------------------------------------------
# ACIContract
# ---------------------------------------------------------------------------


class ACIContractTests(_ContractFixture):
    def test_create_default_scope(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-1")
        self.assertEqual(c.scope, ContractScopeChoices.SCOPE_VRF)

    def test_str(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-1")
        self.assertEqual(str(c), "acme / c-1")

    def test_unique_inside_tenant(self):
        ACIContract.objects.create(aci_tenant=self.tenant, name="dup")
        with self.assertRaises(IntegrityError):
            ACIContract.objects.create(aci_tenant=self.tenant, name="dup")

    def test_same_name_in_different_tenant(self):
        ACIContract.objects.create(aci_tenant=self.tenant, name="shared")
        ACIContract.objects.create(aci_tenant=self.tenant2, name="shared")

    def test_get_absolute_url(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-1")
        self.assertIn("/contracts/", c.get_absolute_url())


# ---------------------------------------------------------------------------
# ACIFilter
# ---------------------------------------------------------------------------


class ACIFilterTests(_ContractFixture):
    def test_create(self):
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-1")
        self.assertEqual(f.aci_tenant, self.tenant)

    def test_str(self):
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-1")
        self.assertEqual(str(f), "acme / f-1")

    def test_unique_inside_tenant(self):
        ACIFilter.objects.create(aci_tenant=self.tenant, name="dup")
        with self.assertRaises(IntegrityError):
            ACIFilter.objects.create(aci_tenant=self.tenant, name="dup")

    def test_same_name_in_different_tenant(self):
        ACIFilter.objects.create(aci_tenant=self.tenant, name="shared")
        ACIFilter.objects.create(aci_tenant=self.common, name="shared")


# ---------------------------------------------------------------------------
# ACIFilterEntry
# ---------------------------------------------------------------------------


class ACIFilterEntryTests(_ContractFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.filter = ACIFilter.objects.create(aci_tenant=cls.tenant, name="f-1")

    def test_create(self):
        e = ACIFilterEntry.objects.create(aci_filter=self.filter, name="e-1")
        self.assertEqual(e.ether_type, ContractFilterEntryEtherTypeChoices.UNSPECIFIED)

    def test_str(self):
        e = ACIFilterEntry.objects.create(aci_filter=self.filter, name="e-1")
        self.assertEqual(str(e), "f-1 / e-1")

    def test_aci_tenant_property(self):
        e = ACIFilterEntry.objects.create(aci_filter=self.filter, name="e-1")
        self.assertEqual(e.aci_tenant, self.tenant)

    def test_unique_inside_filter(self):
        ACIFilterEntry.objects.create(aci_filter=self.filter, name="dup")
        with self.assertRaises(IntegrityError):
            ACIFilterEntry.objects.create(aci_filter=self.filter, name="dup")

    def test_port_pair_requires_both(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-bad",
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
            source_port_from=80,
        )
        with self.assertRaises(ValidationError):
            e.clean()

    def test_port_to_must_be_ge_from(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-bad",
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
            source_port_from=80,
            source_port_to=20,
        )
        with self.assertRaises(ValidationError):
            e.clean()

    def test_port_only_valid_for_tcp_udp(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-bad",
            ip_protocol=ContractFilterEntryIPProtocolChoices.ICMP,
            source_port_from=80,
            source_port_to=80,
        )
        with self.assertRaises(ValidationError):
            e.clean()

    def test_tcp_port_pair_ok(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-ok",
            ether_type=ContractFilterEntryEtherTypeChoices.IP,
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
            source_port_from=80,
            source_port_to=80,
        )
        e.clean()  # must not raise

    def test_arp_opcode_requires_arp_ether(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-arp-bad",
            ether_type=ContractFilterEntryEtherTypeChoices.IP,
            arp_opcode="req",
        )
        with self.assertRaises(ValidationError):
            e.clean()

    def test_icmp_v4_requires_icmp(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-icmp-bad",
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
            icmp_v4_type="echo",
        )
        with self.assertRaises(ValidationError):
            e.clean()

    def test_icmp_v6_requires_icmpv6(self):
        e = ACIFilterEntry(
            aci_filter=self.filter,
            name="e-icmpv6-bad",
            ip_protocol=ContractFilterEntryIPProtocolChoices.TCP,
            icmp_v6_type="echo",
        )
        with self.assertRaises(ValidationError):
            e.clean()


# ---------------------------------------------------------------------------
# ACISubject
# ---------------------------------------------------------------------------


class ACISubjectTests(_ContractFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.contract = ACIContract.objects.create(aci_tenant=cls.tenant, name="c-1")

    def test_create(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-1")
        self.assertTrue(s.apply_both_directions)
        self.assertEqual(s.aci_tenant, self.tenant)

    def test_str(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-1")
        self.assertEqual(str(s), "c-1 / s-1")

    def test_unique_inside_contract(self):
        ACISubject.objects.create(aci_contract=self.contract, name="dup")
        with self.assertRaises(IntegrityError):
            ACISubject.objects.create(aci_contract=self.contract, name="dup")

    def test_reverse_filter_ports_requires_both_directions(self):
        s = ACISubject(
            aci_contract=self.contract,
            name="s-bad",
            apply_both_directions=False,
            reverse_filter_ports=True,
        )
        with self.assertRaises(ValidationError):
            s.clean()

    def test_one_way_no_reverse_ok(self):
        s = ACISubject(
            aci_contract=self.contract,
            name="s-ok",
            apply_both_directions=False,
            reverse_filter_ports=False,
        )
        s.clean()


# ---------------------------------------------------------------------------
# ACISubjectFilter (through-model)
# ---------------------------------------------------------------------------


class ACISubjectFilterTests(_ContractFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.contract = ACIContract.objects.create(aci_tenant=cls.tenant, name="c-1")
        cls.filter = ACIFilter.objects.create(aci_tenant=cls.tenant, name="f-1")
        cls.filter2 = ACIFilter.objects.create(aci_tenant=cls.tenant, name="f-2")

    def test_create_default_both(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-1")
        sf = ACISubjectFilter.objects.create(aci_subject=s, aci_filter=self.filter, name="sf-1")
        self.assertEqual(sf.direction, SubjectFilterDirectionChoices.BOTH)
        self.assertEqual(sf.action, SubjectFilterActionChoices.PERMIT)

    def test_str_uses_ascii_arrow(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-1")
        sf = ACISubjectFilter.objects.create(aci_subject=s, aci_filter=self.filter, name="sf-1")
        self.assertIn("<->", str(sf))

    def test_unique_subject_filter_direction(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-1")
        ACISubjectFilter.objects.create(aci_subject=s, aci_filter=self.filter, name="sf-1")
        with self.assertRaises(IntegrityError):
            ACISubjectFilter.objects.create(aci_subject=s, aci_filter=self.filter, name="sf-2")

    def test_direction_must_be_both_when_subject_two_way(self):
        s = ACISubject.objects.create(
            aci_contract=self.contract,
            name="s-two-way",
            apply_both_directions=True,
        )
        sf = ACISubjectFilter(
            aci_subject=s,
            aci_filter=self.filter,
            name="sf-bad",
            direction=SubjectFilterDirectionChoices.IN,
        )
        with self.assertRaises(ValidationError):
            sf.clean()

    def test_in_out_ok_when_subject_one_way(self):
        s = ACISubject.objects.create(
            aci_contract=self.contract,
            name="s-one-way",
            apply_both_directions=False,
            reverse_filter_ports=False,
        )
        sf = ACISubjectFilter(
            aci_subject=s,
            aci_filter=self.filter,
            name="sf-in",
            direction=SubjectFilterDirectionChoices.IN,
        )
        sf.clean()

    def test_protect_filter(self):
        s = ACISubject.objects.create(aci_contract=self.contract, name="s-prot")
        ACISubjectFilter.objects.create(aci_subject=s, aci_filter=self.filter, name="sf-prot")
        from django.db.models import ProtectedError

        with self.assertRaises(ProtectedError):
            self.filter.delete()


# ---------------------------------------------------------------------------
# ACIContractRelation
# ---------------------------------------------------------------------------


class ACIContractRelationTests(_ContractFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.contract = ACIContract.objects.create(aci_tenant=cls.tenant, name="c-1")
        cls.common_contract = ACIContract.objects.create(aci_tenant=cls.common, name="c-shared")

    def test_xor_requires_one(self):
        r = ACIContractRelation(
            aci_contract=self.contract, role=ContractRelationRoleChoices.PROVIDER
        )
        with self.assertRaises(ValidationError):
            r.clean()

    def test_xor_rejects_both(self):
        r = ACIContractRelation(
            aci_contract=self.contract,
            aci_endpoint_group=self.epg,
            aci_endpoint_security_group=self.esg,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        with self.assertRaises(ValidationError):
            r.clean()

    def test_epg_ok(self):
        r = ACIContractRelation(
            aci_contract=self.contract,
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        r.clean()

    def test_esg_ok(self):
        r = ACIContractRelation(
            aci_contract=self.contract,
            aci_endpoint_security_group=self.esg,
            role=ContractRelationRoleChoices.CONSUMER,
        )
        r.clean()

    def test_cross_tenant_rejected(self):
        # Contract in tenant 'acme', EPG in tenant 'other' → should fail.
        ap2 = ACIAppProfile.objects.create(aci_tenant=self.tenant2, name="ap2")
        vrf2 = ACIVRF.objects.create(aci_tenant=self.tenant2, name="vrf2")
        bd2 = ACIBridgeDomain.objects.create(aci_tenant=self.tenant2, aci_vrf=vrf2, name="bd2")
        epg2 = ACIEndpointGroup.objects.create(
            aci_tenant=self.tenant2,
            aci_app_profile=ap2,
            aci_bridge_domain=bd2,
            name="epg2",
        )
        r = ACIContractRelation(
            aci_contract=self.contract,
            aci_endpoint_group=epg2,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        with self.assertRaises(ValidationError):
            r.clean()

    def test_common_contract_cross_tenant_ok(self):
        r = ACIContractRelation(
            aci_contract=self.common_contract,
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        r.clean()

    def test_unique_epg_role(self):
        ACIContractRelation.objects.create(
            aci_contract=self.contract,
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.PROVIDER,
            name="r-1",
        )
        with self.assertRaises(IntegrityError):
            ACIContractRelation.objects.create(
                aci_contract=self.contract,
                aci_endpoint_group=self.epg,
                role=ContractRelationRoleChoices.PROVIDER,
                name="r-2",
            )

    def test_target_property(self):
        r = ACIContractRelation.objects.create(
            aci_contract=self.contract,
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.PROVIDER,
            name="r-t",
        )
        self.assertEqual(r.target, self.epg)


# ---------------------------------------------------------------------------
# Extra coverage (Bucket B) — missed lines in contract models
# ---------------------------------------------------------------------------


class ACIContractRelationExtraTests(_ContractFixture):
    """Cover missed lines L90, 93-94, 97, 128-130 in relations.py."""

    def test_zero_targets_rejected(self):
        contract = ACIContract.objects.create(aci_tenant=self.tenant, name="c-zero-tgt")
        rel = ACIContractRelation(
            aci_contract=contract,
            name="rel-zero-tgt",
            role=ContractRelationRoleChoices.PROVIDER,
        )
        with self.assertRaisesRegex(ValidationError, "Exactly one"):
            rel.clean()

    def test_two_targets_rejected(self):
        contract = ACIContract.objects.create(aci_tenant=self.tenant, name="c-two-tgt")
        rel = ACIContractRelation(
            aci_contract=contract,
            name="rel-two-tgt",
            aci_endpoint_group=self.epg,
            aci_endpoint_security_group=self.esg,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        with self.assertRaisesRegex(ValidationError, "Exactly one"):
            rel.clean()

    def test_cross_tenant_contract_rejected(self):
        contract2 = ACIContract.objects.create(aci_tenant=self.tenant2, name="c-cross")
        rel = ACIContractRelation(
            aci_contract=contract2,
            name="rel-cross",
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.CONSUMER,
        )
        with self.assertRaisesRegex(ValidationError, "tenant"):
            rel.clean()

    def test_common_tenant_contract_allowed(self):
        common_contract = ACIContract.objects.create(aci_tenant=self.common, name="c-common")
        rel = ACIContractRelation(
            aci_contract=common_contract,
            name="rel-common",
            aci_endpoint_group=self.epg,
            role=ContractRelationRoleChoices.PROVIDER,
        )
        rel.clean()  # Should not raise


class ACIFilterExtraTests(_ContractFixture):
    """Cover get_absolute_url (L46 in filters.py)."""

    def test_get_absolute_url(self):
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-url-extra")
        self.assertIn(str(f.pk), f.get_absolute_url())


class ACIFilterEntryExtraTests(_ContractFixture):
    """Cover get_absolute_url (L153 in filters.py)."""

    def test_get_absolute_url(self):
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-entry-url")
        from netbox_cisco_aci.choices import ContractFilterEntryEtherTypeChoices

        entry = ACIFilterEntry.objects.create(
            aci_filter=f,
            name="entry-url",
            ether_type=ContractFilterEntryEtherTypeChoices.IP,
        )
        self.assertIn(str(entry.pk), entry.get_absolute_url())


class ACISubjectExtraTests(_ContractFixture):
    """Cover get_absolute_url (L88 in subjects.py) and reverse_filter_ports validation."""

    def test_get_absolute_url(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-subj-url")
        subj = ACISubject.objects.create(aci_contract=c, name="subj-url")
        self.assertIn(str(subj.pk), subj.get_absolute_url())

    def test_reverse_filter_ports_requires_both_directions(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-rev-filter")
        from netbox_cisco_aci.models.contracts import ACISubject

        subj = ACISubject(
            aci_contract=c,
            name="subj-rev",
            apply_both_directions=False,
            reverse_filter_ports=True,
        )
        with self.assertRaisesRegex(ValidationError, "reverse_filter_ports"):
            subj.full_clean()


class ACISubjectFilterExtraTests(_ContractFixture):
    """Cover get_absolute_url (L163 in subjects.py) and direction validation."""

    def test_get_absolute_url(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-subj-filt-url")
        subj = ACISubject.objects.create(
            aci_contract=c, name="subj-filt-url", apply_both_directions=True
        )
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-subj-filt-url")
        sf = ACISubjectFilter.objects.create(
            aci_subject=subj,
            aci_filter=f,
            direction=SubjectFilterDirectionChoices.BOTH,
        )
        self.assertIn(str(sf.pk), sf.get_absolute_url())

    def test_direction_must_be_both_when_apply_both_directions(self):
        c = ACIContract.objects.create(aci_tenant=self.tenant, name="c-dir-both")
        subj = ACISubject.objects.create(
            aci_contract=c, name="subj-dir-both", apply_both_directions=True
        )
        f = ACIFilter.objects.create(aci_tenant=self.tenant, name="f-dir-both")
        sf = ACISubjectFilter(
            aci_subject=subj,
            aci_filter=f,
            direction=SubjectFilterDirectionChoices.IN,
        )
        with self.assertRaisesRegex(ValidationError, "direction"):
            sf.full_clean()
