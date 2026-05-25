"""Reusable validators for ACI fields."""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import ACI_POLICY_NAME_REGEX

_POLICY_NAME_RE = re.compile(ACI_POLICY_NAME_REGEX)


def aci_policy_name_validator(value: str) -> None:
    """Validate that a string matches APIC's policy-name regex.

    APIC accepts letters, digits, dot, dash, underscore, and colon.
    Anything else is rejected server-side, so we reject it locally too
    rather than failing on push.
    """

    if not value:
        return
    if not _POLICY_NAME_RE.match(value):
        raise ValidationError(
            _(
                "%(value)s is not a valid ACI policy name. Allowed characters "
                "are letters, digits, and `._:-`."
            ),
            params={"value": value},
        )


def aci_policy_name_optional_validator(value: str) -> None:
    """Same as :func:`aci_policy_name_validator` but tolerates blanks."""

    if not value:
        return
    aci_policy_name_validator(value)


def vlan_id_validator(value: int) -> None:
    """Validate a VLAN encap ID is in the legal ACI range (1–4094)."""

    from .constants import VLAN_ID_MAX, VLAN_ID_MIN

    if not (VLAN_ID_MIN <= value <= VLAN_ID_MAX):
        raise ValidationError(
            _("VLAN ID %(value)s is outside the legal range %(lo)d–%(hi)d."),
            params={"value": value, "lo": VLAN_ID_MIN, "hi": VLAN_ID_MAX},
        )
