"""DRF ViewSets for Switch / Interface Profiles + selectors + attachments (Phase 4)."""

from netbox.api.viewsets import NetBoxModelViewSet

from ...filtersets.access_profiles import (
    ACIInterfaceProfileFilterSet,
    ACIInterfaceProfileSelectorFilterSet,
    ACISwitchProfileFilterSet,
    ACISwitchProfileInterfaceProfileAttachmentFilterSet,
    ACISwitchProfileSelectorFilterSet,
)
from ...models.access import (
    ACIInterfaceProfile,
    ACIInterfaceProfileSelector,
    ACISwitchProfile,
    ACISwitchProfileInterfaceProfileAttachment,
    ACISwitchProfileSelector,
)
from ..serializers.access_profiles import (
    ACIInterfaceProfileSelectorSerializer,
    ACIInterfaceProfileSerializer,
    ACISwitchProfileInterfaceProfileAttachmentSerializer,
    ACISwitchProfileSelectorSerializer,
    ACISwitchProfileSerializer,
)


class ACISwitchProfileViewSet(NetBoxModelViewSet):
    queryset = ACISwitchProfile.objects.select_related("aci_fabric")
    serializer_class = ACISwitchProfileSerializer
    filterset_class = ACISwitchProfileFilterSet


class ACISwitchProfileSelectorViewSet(NetBoxModelViewSet):
    queryset = ACISwitchProfileSelector.objects.select_related(
        "switch_profile", "switch_profile__aci_fabric"
    )
    serializer_class = ACISwitchProfileSelectorSerializer
    filterset_class = ACISwitchProfileSelectorFilterSet


class ACIInterfaceProfileViewSet(NetBoxModelViewSet):
    queryset = ACIInterfaceProfile.objects.select_related("aci_fabric")
    serializer_class = ACIInterfaceProfileSerializer
    filterset_class = ACIInterfaceProfileFilterSet


class ACIInterfaceProfileSelectorViewSet(NetBoxModelViewSet):
    queryset = ACIInterfaceProfileSelector.objects.select_related(
        "interface_profile", "interface_profile__aci_fabric", "policy_group"
    )
    serializer_class = ACIInterfaceProfileSelectorSerializer
    filterset_class = ACIInterfaceProfileSelectorFilterSet


class ACISwitchProfileInterfaceProfileAttachmentViewSet(NetBoxModelViewSet):
    queryset = ACISwitchProfileInterfaceProfileAttachment.objects.select_related(
        "switch_profile", "interface_profile"
    )
    serializer_class = ACISwitchProfileInterfaceProfileAttachmentSerializer
    filterset_class = ACISwitchProfileInterfaceProfileAttachmentFilterSet
