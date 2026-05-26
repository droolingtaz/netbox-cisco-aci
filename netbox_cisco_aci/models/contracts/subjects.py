"""ACI Subject (``vzSubj``) and the SubjectFilter through-model."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...choices import (
    QualityOfServiceClassChoices,
    SubjectFilterActionChoices,
    SubjectFilterDirectionChoices,
    SubjectFilterPriorityChoices,
)
from ..base import ACIBaseModel


class ACISubject(ACIBaseModel):
    """A bundle of filters inside a contract (``vzSubj``).

    A Subject derives its tenancy from its parent Contract.
    """

    aci_contract = models.ForeignKey(
        to="netbox_cisco_aci.ACIContract",
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name=_("ACI Contract"),
    )
    apply_both_directions = models.BooleanField(
        verbose_name=_("Apply both directions"),
        default=True,
        help_text=_(
            "When True, filters apply in both directions on the same subject. "
            "When False, the subject uses separate in-filters and out-filters."
        ),
    )
    reverse_filter_ports = models.BooleanField(
        verbose_name=_("Reverse filter ports"),
        default=True,
        help_text=_(
            "Only meaningful when apply_both_directions is True. "
            "Swaps source/destination ports for the reverse direction."
        ),
    )
    qos_class = models.CharField(
        verbose_name=_("QoS class"),
        max_length=16,
        blank=True,
        choices=QualityOfServiceClassChoices,
    )
    target_dscp = models.CharField(
        verbose_name=_("Target DSCP"),
        max_length=32,
        blank=True,
    )
    filters = models.ManyToManyField(
        to="netbox_cisco_aci.ACIFilter",
        through="netbox_cisco_aci.ACISubjectFilter",
        related_name="subjects",
        blank=True,
        verbose_name=_("Filters"),
    )

    clone_fields = (
        "aci_contract",
        "apply_both_directions",
        "reverse_filter_ports",
        "qos_class",
        "target_dscp",
        "description",
    )

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Subject")
        verbose_name_plural = _("ACI Subjects")
        ordering = ("aci_contract", "name")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_contract", "name"),
                name="netbox_cisco_aci_acisubject_contract_name_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_contract.name} / {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisubject", args=[self.pk])

    @property
    def aci_tenant(self):
        return self.aci_contract.aci_tenant

    def clean(self) -> None:
        super().clean()
        if not self.apply_both_directions and self.reverse_filter_ports:
            raise ValidationError(
                {
                    "reverse_filter_ports": _(
                        "`reverse_filter_ports` is only meaningful when "
                        "`apply_both_directions` is True."
                    )
                }
            )


class ACISubjectFilter(ACIBaseModel):
    """Through-model linking a Subject to a Filter.

    There is no direct APIC analogue — this captures the metadata APIC
    keeps on the ``vzRsSubjFiltAtt`` / ``vzInTerm`` / ``vzOutTerm``
    relationships (direction, action, priority).
    """

    aci_subject = models.ForeignKey(
        to="netbox_cisco_aci.ACISubject",
        on_delete=models.CASCADE,
        related_name="filter_attachments",
        verbose_name=_("ACI Subject"),
    )
    aci_filter = models.ForeignKey(
        to="netbox_cisco_aci.ACIFilter",
        on_delete=models.PROTECT,
        related_name="subject_attachments",
        verbose_name=_("ACI Filter"),
    )
    direction = models.CharField(
        verbose_name=_("Direction"),
        max_length=8,
        default=SubjectFilterDirectionChoices.BOTH,
        choices=SubjectFilterDirectionChoices,
    )
    action = models.CharField(
        verbose_name=_("Action"),
        max_length=16,
        default=SubjectFilterActionChoices.PERMIT,
        choices=SubjectFilterActionChoices,
    )
    priority = models.CharField(
        verbose_name=_("Priority"),
        max_length=16,
        default=SubjectFilterPriorityChoices.DEFAULT,
        choices=SubjectFilterPriorityChoices,
    )

    clone_fields = ("aci_subject", "aci_filter", "direction", "action", "priority")

    class Meta(ACIBaseModel.Meta):
        verbose_name = _("ACI Subject Filter")
        verbose_name_plural = _("ACI Subject Filters")
        ordering = ("aci_subject", "aci_filter", "direction")
        constraints = (
            models.UniqueConstraint(
                fields=("aci_subject", "aci_filter", "direction"),
                name="netbox_cisco_aci_acisubjectfilter_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.aci_subject.name} <-> {self.aci_filter.name} ({self.direction})"

    def get_absolute_url(self) -> str:
        return reverse("plugins:netbox_cisco_aci:acisubjectfilter", args=[self.pk])

    def clean(self) -> None:
        super().clean()
        if (
            self.aci_subject_id
            and self.aci_subject.apply_both_directions
            and self.direction != SubjectFilterDirectionChoices.BOTH
        ):
            raise ValidationError(
                {
                    "direction": _(
                        "When the Subject applies in both directions, "
                        "the attachment direction must be `both`."
                    )
                }
            )
