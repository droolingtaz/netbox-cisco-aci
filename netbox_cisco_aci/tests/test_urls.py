"""URL resolution sanity tests.

These exist because NetBox 4.x detail and list-row templates reverse
``<label>_changelog`` and ``<label>_journal`` unconditionally. A plugin
that registers the basic CRUD verbs but forgets the changelog / journal
routes (as we did for the very first cut of the plugin's URL patterns)
will silently pass ``NetBoxModelViewTestCase.*`` because those test
classes only reverse the explicit verbs they cover. The user only
discovers the gap when they click on a list page in a real browser
and gets a 500-error page from ``django.urls.exceptions.NoReverseMatch``.

The tests below close that loop: every model in the plugin must expose
the full ten-route block (list / add / import / bulk-edit / bulk-delete /
detail / edit / delete / **changelog** / **journal**) and each route
must resolve cleanly.
"""

from django.test import TestCase
from django.urls import NoReverseMatch, reverse

# Every UI-bearing model in the plugin, identified by the label passed
# to ``_crud(...)`` in netbox_cisco_aci/urls.py. When a new model is
# added, the entry must be added here too — this list is the simplest
# regression guard we have for "a brand-new model wires up its CRUD
# routes but forgets changelog/journal".
PLUGIN_MODELS = [
    # Phase 1 — Fabric
    "acifabric",
    "acipod",
    "acinode",
    # Phase 2 — Tenancy
    "acitenant",
    "acivrf",
    "acibridgedomain",
    "acibridgedomainsubnet",
    "aciappprofile",
    "aciendpointgroup",
    "aciusegattribute",
    "aciendpointsecuritygroup",
    # Phase 3 — Access Phase A
    "acivlanpool",
    "acivlanpoolblock",
    "acidomain",
    "aciaaep",
    "aciaaepepgmapping",
    # Phase 4 — Access Phase B
    "acilinklevelpolicy",
    "acicdpinterfacepolicy",
    "acilldpinterfacepolicy",
    "acilacpinterfacepolicy",
    "acimcpinterfacepolicy",
    "acistpinterfacepolicy",
    "aciinterfacepolicygroup",
    "aciswitchprofile",
    "aciswitchprofileselector",
    "aciinterfaceprofile",
    "aciinterfaceprofileselector",
    "aciswitchprofileinterfaceprofileattachment",
    # Phase 5 — Contracts
    "acicontract",
    "acisubject",
    "acifilter",
    "acifilterentry",
    "acisubjectfilter",
    "acicontractrelation",
    # Phase 6 — Bindings
    "acistaticportbinding",
    "acivpcbindingpair",
    "acidomainbinding",
    "aciinterfacefabricmembership",
    # Phase 7 — L3Outs
    "acil3out",
    "acilogicalnodeprofile",
    "acilogicalnode",
    "acilogicalinterfaceprofile",
    "acil3outinterface",
    "acibgppeer",
    "aciospfinterfacepolicy",
    "aciospfinterfaceattachment",
    "acieigrpinterfacepolicy",
    "aciexternalepg",
    "aciexternalepgsubnet",
    # Phase 7.1 — Static routes
    "acil3outstaticroute",
    "acil3outstaticroutenexthop",
]


class PluginURLPatternsTests(TestCase):
    """Every model's ten standard routes must resolve."""

    # The five routes that don't take a pk argument.
    PK_LESS = ["list", "add", "import", "bulk_edit", "bulk_delete"]

    # The five routes that take a single pk argument.
    PK_BOUND = ["", "edit", "delete", "changelog", "journal"]

    def _name(self, label, suffix):
        return f"plugins:netbox_cisco_aci:{label}{('_' + suffix) if suffix else ''}"

    def test_all_models_expose_pk_less_routes(self):
        for label in PLUGIN_MODELS:
            for suffix in self.PK_LESS:
                with self.subTest(label=label, suffix=suffix):
                    try:
                        reverse(self._name(label, suffix))
                    except NoReverseMatch as exc:
                        self.fail(f"reverse() failed for {label}_{suffix}: {exc}")

    def test_all_models_expose_pk_bound_routes(self):
        for label in PLUGIN_MODELS:
            for suffix in self.PK_BOUND:
                with self.subTest(label=label, suffix=suffix):
                    try:
                        reverse(self._name(label, suffix), kwargs={"pk": 1})
                    except NoReverseMatch as exc:
                        self.fail(f"reverse() failed for {label}_{suffix}: {exc}")

    def test_changelog_and_journal_routes_resolve(self):
        """Explicit, dedicated coverage for the routes that triggered
        the original 500 the user hit: the production crash was
        ``Reverse for 'acifabric_changelog' not found``, so we want a
        named test that fails loudly if those two routes ever
        regress."""
        for label in PLUGIN_MODELS:
            for suffix in ("changelog", "journal"):
                with self.subTest(label=label, suffix=suffix):
                    url = reverse(self._name(label, suffix), kwargs={"pk": 1})
                    self.assertTrue(
                        url.endswith(f"/{suffix}/"),
                        f"{label}_{suffix} resolved to {url!r} which does not end with /{suffix}/",
                    )
