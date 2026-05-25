"""UI views for fabric-topology models."""

from netbox.views import generic

from ..filtersets.fabric import ACIFabricFilterSet, ACINodeFilterSet, ACIPodFilterSet
from ..forms.fabric import (
    ACIFabricBulkEditForm,
    ACIFabricFilterForm,
    ACIFabricForm,
    ACIFabricImportForm,
    ACINodeBulkEditForm,
    ACINodeFilterForm,
    ACINodeForm,
    ACINodeImportForm,
    ACIPodBulkEditForm,
    ACIPodFilterForm,
    ACIPodForm,
    ACIPodImportForm,
)
from ..models.fabric import ACIFabric, ACINode, ACIPod
from ..tables.fabric import ACIFabricTable, ACINodeTable, ACIPodTable

# ---------------------------------------------------------------------------
# ACIFabric
# ---------------------------------------------------------------------------


class ACIFabricView(generic.ObjectView):
    queryset = ACIFabric.objects.all()


class ACIFabricListView(generic.ObjectListView):
    queryset = ACIFabric.objects.all()
    table = ACIFabricTable
    filterset = ACIFabricFilterSet
    filterset_form = ACIFabricFilterForm


class ACIFabricEditView(generic.ObjectEditView):
    queryset = ACIFabric.objects.all()
    form = ACIFabricForm


class ACIFabricDeleteView(generic.ObjectDeleteView):
    queryset = ACIFabric.objects.all()


class ACIFabricBulkImportView(generic.BulkImportView):
    queryset = ACIFabric.objects.all()
    model_form = ACIFabricImportForm


class ACIFabricBulkEditView(generic.BulkEditView):
    queryset = ACIFabric.objects.all()
    filterset = ACIFabricFilterSet
    table = ACIFabricTable
    form = ACIFabricBulkEditForm


class ACIFabricBulkDeleteView(generic.BulkDeleteView):
    queryset = ACIFabric.objects.all()
    filterset = ACIFabricFilterSet
    table = ACIFabricTable


# ---------------------------------------------------------------------------
# ACIPod
# ---------------------------------------------------------------------------


class ACIPodView(generic.ObjectView):
    queryset = ACIPod.objects.select_related("aci_fabric")


class ACIPodListView(generic.ObjectListView):
    queryset = ACIPod.objects.select_related("aci_fabric")
    table = ACIPodTable
    filterset = ACIPodFilterSet
    filterset_form = ACIPodFilterForm


class ACIPodEditView(generic.ObjectEditView):
    queryset = ACIPod.objects.all()
    form = ACIPodForm


class ACIPodDeleteView(generic.ObjectDeleteView):
    queryset = ACIPod.objects.all()


class ACIPodBulkImportView(generic.BulkImportView):
    queryset = ACIPod.objects.all()
    model_form = ACIPodImportForm


class ACIPodBulkEditView(generic.BulkEditView):
    queryset = ACIPod.objects.all()
    filterset = ACIPodFilterSet
    table = ACIPodTable
    form = ACIPodBulkEditForm


class ACIPodBulkDeleteView(generic.BulkDeleteView):
    queryset = ACIPod.objects.all()
    filterset = ACIPodFilterSet
    table = ACIPodTable


# ---------------------------------------------------------------------------
# ACINode
# ---------------------------------------------------------------------------


class ACINodeView(generic.ObjectView):
    queryset = ACINode.objects.select_related("aci_pod", "aci_pod__aci_fabric")


class ACINodeListView(generic.ObjectListView):
    queryset = ACINode.objects.select_related("aci_pod", "aci_pod__aci_fabric")
    table = ACINodeTable
    filterset = ACINodeFilterSet
    filterset_form = ACINodeFilterForm


class ACINodeEditView(generic.ObjectEditView):
    queryset = ACINode.objects.all()
    form = ACINodeForm


class ACINodeDeleteView(generic.ObjectDeleteView):
    queryset = ACINode.objects.all()


class ACINodeBulkImportView(generic.BulkImportView):
    queryset = ACINode.objects.all()
    model_form = ACINodeImportForm


class ACINodeBulkEditView(generic.BulkEditView):
    queryset = ACINode.objects.all()
    filterset = ACINodeFilterSet
    table = ACINodeTable
    form = ACINodeBulkEditForm


class ACINodeBulkDeleteView(generic.BulkDeleteView):
    queryset = ACINode.objects.all()
    filterset = ACINodeFilterSet
    table = ACINodeTable
