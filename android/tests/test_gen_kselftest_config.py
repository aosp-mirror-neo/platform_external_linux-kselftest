# Copyright (C) 2026 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for kselftest VTS configuration generator."""

import os
import sys
import unittest
import xml.etree.ElementTree as ET

# Add android/ directory to sys.path
ANDROID_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ANDROID_DIR not in sys.path:
    sys.path.insert(0, ANDROID_DIR)

from configs.disabled_tests import DISABLED_TESTS
from configs.mandatory_tests import MANDATORY_TESTS
from configs.test_definitions import ALL_TEST_CASES
import gen_kselftest_config


class GenKselftestConfigTest(unittest.TestCase):

    def setUp(self):
        with open(gen_kselftest_config.DEFAULT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
            self.template = f.read()

    def test_all_tests_have_mandatory_definition(self):
        """Every enabled test in ALL_TEST_CASES must be defined in MANDATORY_TESTS."""
        for test in ALL_TEST_CASES:
            if test.base_name in DISABLED_TESTS:
                continue
            self.assertIn(
                test.base_name,
                MANDATORY_TESTS,
                f"Test '{test.base_name}' is missing in MANDATORY_TESTS dictionary."
            )

    def test_configs_collide(self):
        """A disabled test must not also be listed in MANDATORY_TESTS."""
        collisions = sorted(set(MANDATORY_TESTS) & set(DISABLED_TESTS))
        self.assertEqual(
            collisions, [],
            f"Tests listed in both MANDATORY_TESTS and DISABLED_TESTS: {collisions}"
        )

    def test_config_keys_exist_in_catalog(self):
        """Every MANDATORY_TESTS / DISABLED_TESTS key must be defined in ALL_TEST_CASES."""
        names = {test.base_name for test in ALL_TEST_CASES}
        self.assertEqual(
            sorted(set(MANDATORY_TESTS) - names), [],
            "MANDATORY_TESTS has entries that are not defined in ALL_TEST_CASES."
        )
        self.assertEqual(
            sorted(set(DISABLED_TESTS) - names), [],
            "DISABLED_TESTS has entries that are not defined in ALL_TEST_CASES."
        )

    def test_generated_xml_is_well_formed(self):
        """Generated XML for every supported architecture must be valid XML."""
        for arch in gen_kselftest_config.SUPPORTED_ARCHES:
            xml_str = gen_kselftest_config.generate_xml_content(arch, self.template)
            # Ensure it can be parsed as valid XML
            try:
                root = ET.fromstring(xml_str)
            except ET.ParseError as e:
                self.fail(f"Generated XML for {arch} is not well-formed: {e}")

            self.assertEqual(root.tag, "configuration")

    def test_dual_kernel_target_test_blocks(self):
        """XML must contain two KernelTargetTest blocks: Mandatory and Skippable."""
        for arch in gen_kselftest_config.SUPPORTED_ARCHES:
            xml_str = gen_kselftest_config.generate_xml_content(arch, self.template)
            root = ET.fromstring(xml_str)
            tests = root.findall("test")
            self.assertEqual(len(tests), 2, f"Arch {arch} should have exactly 2 <test> blocks.")

            # Block 0: Mandatory (No exit-code-skip)
            mandatory_block = tests[0]
            self.assertIsNone(
                mandatory_block.find('option[@name="exit-code-skip"]'),
                f"Mandatory block for {arch} should NOT have exit-code-skip."
            )
            mand_options = mandatory_block.findall('option[@name="test-command-line"]')
            self.assertGreater(len(mand_options), 0, f"Mandatory block for {arch} should not be empty.")

            # Block 1: Skippable (exit-code-skip = 4)
            skippable_block = tests[1]
            skip_opt = skippable_block.find('option[@name="exit-code-skip"]')
            self.assertIsNotNone(
                skip_opt,
                f"Skippable block for {arch} must have exit-code-skip."
            )
            self.assertEqual(skip_opt.get("value"), "4")
            skip_options = skippable_block.findall('option[@name="test-command-line"]')
            self.assertGreater(len(skip_options), 0, f"Skippable block for {arch} should not be empty.")

    def test_disabled_test_excluded(self):
        """Tests listed in DISABLED_TESTS must not appear in any generated XML."""
        # Temporarily mock a disabled test
        test_to_disable = ALL_TEST_CASES[0].base_name
        try:
            DISABLED_TESTS[test_to_disable] = "b/12345678"
            for arch in gen_kselftest_config.SUPPORTED_ARCHES:
                xml_str = gen_kselftest_config.generate_xml_content(arch, self.template)
                self.assertNotIn(
                    f'key="{test_to_disable}_{arch}"',
                    xml_str,
                    f"Disabled test {test_to_disable} was found in {arch} XML."
                )
        finally:
            del DISABLED_TESTS[test_to_disable]

    def test_min_kernel_version_present(self):
        """futex_functional_run.sh must include min-kernel-version 5.1 on supported arches."""
        futex = next(t for t in ALL_TEST_CASES if t.base_name == "futex_functional_run.sh")
        for arch in gen_kselftest_config.SUPPORTED_ARCHES:
            if not futex.is_supported_on(arch):
                continue
            xml_str = gen_kselftest_config.generate_xml_content(arch, self.template)
            root = ET.fromstring(xml_str)
            futex_min_ver = root.find(f'.//option[@key="futex_functional_run.sh_{arch}"][@name="min-kernel-version"]')
            self.assertIsNotNone(futex_min_ver, f"min-kernel-version missing for futex on {arch}")
            self.assertEqual(futex_min_ver.get("value"), "5.1")


if __name__ == "__main__":
    unittest.main()
