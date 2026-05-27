"""Tests for netbox_cisco_aci.validators (Bucket C)."""

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from netbox_cisco_aci.validators import (
    aci_policy_name_optional_validator,
    aci_policy_name_validator,
    vlan_id_validator,
)


class ACIPolicyNameValidatorTests(SimpleTestCase):
    """Cover aci_policy_name_validator — L22, 36-38, 44, 46-47 in validators.py."""

    def test_valid_names_do_not_raise(self):
        valid = ["good", "good-name", "good_name", "good.name", "abc123", "A:B", "x.y:z-w_1"]
        for name in valid:
            aci_policy_name_validator(name)  # must not raise

    def test_invalid_chars_raise_validation_error(self):
        invalid = ["bad name", "bad@name", "bad/name", "bad!name", "bad#name"]
        for name in invalid:
            with self.assertRaises(ValidationError, msg=f"Expected ValidationError for {name!r}"):
                aci_policy_name_validator(name)

    def test_empty_string_does_not_raise(self):
        """Empty string is allowed by aci_policy_name_validator (early return on L22)."""
        aci_policy_name_validator("")  # must not raise

    def test_space_raises(self):
        with self.assertRaisesRegex(ValidationError, "policy name"):
            aci_policy_name_validator("has space")

    def test_slash_raises(self):
        with self.assertRaisesRegex(ValidationError, "policy name"):
            aci_policy_name_validator("has/slash")

    def test_at_sign_raises(self):
        with self.assertRaisesRegex(ValidationError, "policy name"):
            aci_policy_name_validator("bad@char")


class ACIPolicyNameOptionalValidatorTests(SimpleTestCase):
    """Cover aci_policy_name_optional_validator — delegates to base validator."""

    def test_blank_is_always_ok(self):
        aci_policy_name_optional_validator("")  # must not raise

    def test_valid_name_passes(self):
        aci_policy_name_optional_validator("valid-name")

    def test_invalid_name_raises(self):
        with self.assertRaises(ValidationError):
            aci_policy_name_optional_validator("bad name")


class VLANIDValidatorTests(SimpleTestCase):
    """Cover vlan_id_validator — L44, 46-47 in validators.py."""

    def test_valid_vlan_ids_pass(self):
        for vid in [1, 100, 1000, 4094]:
            vlan_id_validator(vid)  # must not raise

    def test_vlan_0_raises(self):
        with self.assertRaisesRegex(ValidationError, "legal range"):
            vlan_id_validator(0)

    def test_vlan_4095_raises(self):
        with self.assertRaisesRegex(ValidationError, "legal range"):
            vlan_id_validator(4095)

    def test_negative_vlan_raises(self):
        with self.assertRaisesRegex(ValidationError, "legal range"):
            vlan_id_validator(-1)
