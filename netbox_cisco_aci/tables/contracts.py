"""Tables for Phase 5 contract / filter / relation models."""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from ..models.contracts import (
    ACIContract,
    ACIContractRelation,
    ACIFilter,
    ACIFilterEntry,
    ACISubject,
    ACISubjectFilter,
)


class ACIContractTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    scope = ChoiceFieldColumn()
    qos_class = ChoiceFieldColumn(verbose_name="QoS")
    subject_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acisubject_list",
        url_params={"aci_contract_id": "pk"},
        verbose_name="Subjects",
    )
    relation_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acicontractrelation_list",
        url_params={"aci_contract_id": "pk"},
        verbose_name="Relations",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acicontract_list")

    class Meta(NetBoxTable.Meta):
        model = ACIContract
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "scope",
            "qos_class",
            "target_dscp",
            "subject_count",
            "relation_count",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_tenant",
            "scope",
            "subject_count",
            "relation_count",
        )


class ACISubjectTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_contract = tables.Column(linkify=True, verbose_name="Contract")
    apply_both_directions = columns.BooleanColumn(verbose_name="Both dirs")
    reverse_filter_ports = columns.BooleanColumn(verbose_name="Reverse")
    qos_class = ChoiceFieldColumn(verbose_name="QoS")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acisubject_list")

    class Meta(NetBoxTable.Meta):
        model = ACISubject
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_contract",
            "apply_both_directions",
            "reverse_filter_ports",
            "qos_class",
            "target_dscp",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_contract", "apply_both_directions", "qos_class")


class ACIFilterTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_tenant = tables.Column(linkify=True, verbose_name="Tenant")
    entry_count = columns.LinkedCountColumn(
        viewname="plugins:netbox_cisco_aci:acifilterentry_list",
        url_params={"aci_filter_id": "pk"},
        verbose_name="Entries",
    )
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acifilter_list")

    class Meta(NetBoxTable.Meta):
        model = ACIFilter
        fields = (
            "pk",
            "id",
            "name",
            "name_alias",
            "aci_tenant",
            "entry_count",
            "description",
            "tags",
        )
        default_columns = ("name", "aci_tenant", "entry_count")


class ACIFilterEntryTable(NetBoxTable):
    name = tables.Column(linkify=True)
    aci_filter = tables.Column(linkify=True, verbose_name="Filter")
    ether_type = ChoiceFieldColumn()
    ip_protocol = ChoiceFieldColumn(verbose_name="IP protocol")
    source_port_from = tables.Column(verbose_name="Src from")
    source_port_to = tables.Column(verbose_name="Src to")
    destination_port_from = tables.Column(verbose_name="Dst from")
    destination_port_to = tables.Column(verbose_name="Dst to")
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acifilterentry_list")

    class Meta(NetBoxTable.Meta):
        model = ACIFilterEntry
        fields = (
            "pk",
            "id",
            "name",
            "aci_filter",
            "ether_type",
            "ip_protocol",
            "source_port_from",
            "source_port_to",
            "destination_port_from",
            "destination_port_to",
            "tcp_rules",
            "stateful",
            "match_only_fragments",
            "arp_opcode",
            "icmp_v4_type",
            "icmp_v6_type",
            "description",
            "tags",
        )
        default_columns = (
            "name",
            "aci_filter",
            "ether_type",
            "ip_protocol",
            "destination_port_from",
            "destination_port_to",
        )


class ACISubjectFilterTable(NetBoxTable):
    aci_subject = tables.Column(linkify=True, verbose_name="Subject")
    aci_filter = tables.Column(linkify=True, verbose_name="Filter")
    direction = ChoiceFieldColumn()
    action = ChoiceFieldColumn()
    priority = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acisubjectfilter_list")

    class Meta(NetBoxTable.Meta):
        model = ACISubjectFilter
        fields = (
            "pk",
            "id",
            "aci_subject",
            "aci_filter",
            "direction",
            "action",
            "priority",
            "name",
            "description",
            "tags",
        )
        default_columns = (
            "aci_subject",
            "aci_filter",
            "direction",
            "action",
            "priority",
        )


class ACIContractRelationTable(NetBoxTable):
    aci_contract = tables.Column(linkify=True, verbose_name="Contract")
    aci_endpoint_group = tables.Column(linkify=True, verbose_name="EPG")
    aci_endpoint_security_group = tables.Column(linkify=True, verbose_name="ESG")
    role = ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_cisco_aci:acicontractrelation_list")

    class Meta(NetBoxTable.Meta):
        model = ACIContractRelation
        fields = (
            "pk",
            "id",
            "aci_contract",
            "aci_endpoint_group",
            "aci_endpoint_security_group",
            "role",
            "name",
            "description",
            "tags",
        )
        default_columns = (
            "aci_contract",
            "role",
            "aci_endpoint_group",
            "aci_endpoint_security_group",
        )
