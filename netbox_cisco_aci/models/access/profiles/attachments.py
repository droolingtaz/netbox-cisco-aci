"""Switch \u2194 Interface Profile through model."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel


class ACISwitchProfileInterfaceProfileAttachment(NetBoxModel):
    """A Switch Profile \u21c4 Interface Profile attachment.

    Modeled as a real through table (not an auto-through) so future
    columns (deployment order, override flags) have somewhere to live.
    Inherits :class:`NetBoxModel` so the attachment can carry tags,
    custom fields and be exposed through NetBox's standard UI/API.
    """

    switch_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACISwitchProfile",
        on_delete=models.CASCADE,
        related_name="interface_profile_attachments",
        verbose_name=_("Switch Profile"),
    )
    interface_profile = models.ForeignKey(
        to="netbox_cisco_aci.ACIInterfaceProfile",
        on_delete=models.CASCADE,
        related_name="switch_profile_attachments",
        verbose_name=_("Interface Profile"),
    )

    clone_fields = ("switch_profile", "interface_profile")

    class Meta:
        verbose_name = _("ACI Switch \u2194 Interface Profile Attachment")
        verbose_name_plural = _("ACI Switch \u2194 Interface Profile Attachments")
        ordering = ("switch_profile", "interface_profile")
        constraints = (
            models.UniqueConstraint(
                fields=("switch_profile", "interface_profile"),
                name="netbox_cisco_aci_aciswiprofattach_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.switch_profile.name} \u2194 {self.interface_profile.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            "plugins:netbox_cisco_aci:aciswitchprofileinterfaceprofileattachment",
            args=[self.pk],
        )

    def clean(self) -> None:
        super().clean()
        if self.switch_profile_id and self.interface_profile_id:
            if self.switch_profile.aci_fabric_id != self.interface_profile.aci_fabric_id:
                raise ValidationError(
                    _("Switch Profile and Interface Profile must belong to the same Fabric.")
                )
