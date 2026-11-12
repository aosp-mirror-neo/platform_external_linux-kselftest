#!/usr/bin/env python3
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

"""Generates or verifies VTS Tradefed XML configs for kselftest."""

import argparse
import difflib
import os
import sys

from configs.disabled_tests import DISABLED_TESTS
from configs.mandatory_tests import MANDATORY_TESTS
from configs.test_definitions import ALL_TEST_CASES

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_TEMPLATE_FILE = os.path.join(
    SCRIPT_DIR, "templates", "vts_linux_kselftest.xml.template"
)

SUPPORTED_ARCHES = {
    "arm_64": "arm64",
    "arm_32": "arm",
    "x86_64": "x86_64",
    "x86_32": "x86",
    "riscv_64": "riscv64",
}


def generate_xml_content(arch_key: str, template: str) -> str:
  """Generates the VTS XML content for the given architecture key."""
  module_arch = SUPPORTED_ARCHES[arch_key]
  mandatory_options = []
  skippable_options = []

  for test in ALL_TEST_CASES:
    # Skip tests that are explicitly disabled
    if test.base_name in DISABLED_TESTS:
      continue

    # Skip tests not supported on this architecture
    if not test.is_supported_on(arch_key):
      continue

    if test.base_name not in MANDATORY_TESTS:
      raise ValueError(
          f"Test '{test.base_name}' is not configured in mandatory_tests.py"
      )

    is_mandatory = MANDATORY_TESTS[test.base_name]
    test_key = f"{test.base_name}_{arch_key}"
    cmd = test.command

    lines = [
        f'        <option name="test-command-line" key="{test_key}"'
        f' value="{cmd}" />'
    ]
    if test.min_kernel_version:
      lines.append(
          f'        <option name="min-kernel-version" key="{test_key}"'
          f' value="{test.min_kernel_version}" />'
      )

    target_list = mandatory_options if is_mandatory else skippable_options
    target_list.extend(lines)

  # Construct XML block strings
  mandatory_block = (
      "\n".join(mandatory_options) if mandatory_options else "        <!-- None -->"
  )
  skippable_block = (
      "\n".join(skippable_options) if skippable_options else "        <!-- None -->"
  )

  return template.format(
      MODULE="{MODULE}",
      MODULE_ARCH=module_arch,
      MANDATORY_TEST_OPTIONS=mandatory_block,
      SKIPPABLE_TEST_OPTIONS=skippable_block,
  )


def xml_filename(arch_key: str) -> str:
  """Returns the file name of the checked-in XML for the architecture key."""
  return f"vts_linux_kselftest_{arch_key}.xml"


def diff_against_generated(
    arch_key: str, template: str, xml_path: str
) -> list[str]:
  """Compares an XML file on disk with the generator output.

  Args:
    arch_key: Architecture key in SUPPORTED_ARCHES.
    template: Content of the XML template.
    xml_path: Path of the XML file to compare.

  Returns:
    Unified diff lines from the file on disk to the generator output, or an
    empty list if the file is up to date.
  """
  with open(xml_path, "r", encoding="utf-8") as f:
    current = f.read()
  generated = generate_xml_content(arch_key, template)
  if current == generated:
    return []

  name = os.path.basename(xml_path)
  return list(
      difflib.unified_diff(
          current.splitlines(keepends=True),
          generated.splitlines(keepends=True),
          fromfile=f"{name} (on disk)",
          tofile=f"{name} (generated)",
      )
  )


def parse_args():
  parser = argparse.ArgumentParser(
      description="Generate or check kselftest VTS Tradefed configs."
  )
  parser.add_argument(
      "--arch",
      choices=list(SUPPORTED_ARCHES.keys()),
      help="Specific architecture to generate/check (defaults to all).",
  )
  parser.add_argument(
      "--template",
      default=DEFAULT_TEMPLATE_FILE,
      help="Path to XML template file.",
  )
  parser.add_argument(
      "--out_dir",
      default=SCRIPT_DIR,
      help="Output directory for generated XML files (defaults to android/).",
  )
  parser.add_argument(
      "--check",
      action="store_true",
      help=(
          "Verify existing files on disk match the generator output without"
          " modifying them."
      ),
  )
  return parser.parse_args()


def main():
  args = parse_args()

  if not os.path.isfile(args.template):
    print(f"Error: Template file not found: {args.template}", file=sys.stderr)
    sys.exit(1)

  with open(args.template, "r", encoding="utf-8") as f:
    template = f.read()

  arches = [args.arch] if args.arch else list(SUPPORTED_ARCHES.keys())
  has_diff = False

  for arch_key in arches:
    filename = xml_filename(arch_key)
    xml_path = os.path.join(args.out_dir, filename)

    if args.check:
      if not os.path.exists(xml_path):
        print(f"[CHECK FAILED] Missing file: {xml_path}", file=sys.stderr)
        has_diff = True
        continue

      diff = diff_against_generated(arch_key, template, xml_path)
      if diff:
        print(
            f"[CHECK FAILED] Config out of sync for {filename}:",
            file=sys.stderr,
        )
        sys.stderr.writelines(diff)
        has_diff = True
      else:
        print(f"[CHECK OK] {filename} is up to date.")
    else:
      generated = generate_xml_content(arch_key, template)
      os.makedirs(os.path.dirname(os.path.abspath(xml_path)), exist_ok=True)
      with open(xml_path, "w", encoding="utf-8") as f:
        f.write(generated)
      print(f"[GENERATED] {xml_path}")

  if args.check and has_diff:
    print(
        "\nERROR: VTS test configurations are out of date.\nRun"
        " 'python3 android/gen_kselftest_config.py' to regenerate them.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
  main()
