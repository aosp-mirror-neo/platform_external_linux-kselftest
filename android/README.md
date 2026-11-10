# VTS Linux kselftest Configuration Framework

This directory contains the Tradefed configuration generator and test definitions for `vts_linux_kselftest` in Android VTS.

The framework is modeled after the LTP configuration architecture to provide declarative test management, clear separation between mandatory and skippable tests, and centralized test disabling.

---

## Architecture Overview

```
android/
├── configs/
│   ├── disabled_tests.py     # Registry of disabled tests with bug references
│   ├── mandatory_tests.py    # Mandatory vs skippable mapping of enabled tests
│   └── test_definitions.py   # Master catalog of test commands and requirements
├── templates/
│   └── vts_linux_kselftest.xml.template  # Dual-block Tradefed configuration template
├── tests/
│   └── test_gen_kselftest_config.py      # Unit tests validating configs and XMLs
├── gen_kselftest_config.py   # Generator script with CI drift verification support
└── README.md                 # This documentation
```

### Key Concepts

1. **Declarative Test Catalog (`configs/test_definitions.py`)**:
   Defines all available kselftest test cases, their execution commands, supported architectures (`arm_64`, `arm_32`, `x86_64`, `x86_32`, `riscv_64`), and minimum kernel version requirements (`min-kernel-version`).

2. **Mandatory vs. Skippable Separation (`configs/mandatory_tests.py`)**:
   * **Mandatory Tests (`True`)**: Core kernel features that must pass on all Android devices. In the generated Tradefed XML, these run **without** `exit-code-skip`. Any non-zero exit code (including `KSFT_SKIP` / exit code 4) is reported as a test failure (`testFailed`).
   * **Skippable Tests (`False`)**: Hardware-dependent or optional kernel features (e.g. RTC alarms, CPU hotplug, KVM memory wiping). In the generated XML, these run with `<option name="exit-code-skip" value="4" />`. An exit code of 4 is reported as `testIgnored`, keeping postsubmit CI green when the underlying hardware or feature is absent.

3. **Centralized Disablement (`configs/disabled_tests.py`)**:
   Tests that are known broken or flaky are centrally tracked in `DISABLED_TESTS` with an explicit Buganizer Bug ID and rationale. Disabled tests are completely omitted from the generated XMLs. A disabled test must not also be listed in `MANDATORY_TESTS`; the unit tests enforce this.

4. **CI Drift Detection (`gen_kselftest_config.py --check`)**:
   Enforces that checked-in XML files (`vts_linux_kselftest_<arch>.xml`) strictly match the Python configuration files. The `gen_kselftest_config_test` host test runs the same check and is listed in the `presubmit` group of `TEST_MAPPING`, so a change that edits `configs/` without regenerating the XMLs, or edits an XML by hand, fails presubmit.

---

## Developer Workflows

### 1. Disabling a Broken or Flaky Test

When a test is failing in CI and requires temporary disabling:

1. Open `android/configs/disabled_tests.py`.
2. Add the test name with its Buganizer Bug ID and explanation:
   ```python
   DISABLED_TESTS = {
       'some_broken_test': 'b/123456789: Description of failure or reason',
   }
   ```
3. Remove the test's entry from `android/configs/mandatory_tests.py` (add it back with its classification when the test is re-enabled).
4. Regenerate the XML configurations:
   ```bash
   python3 android/gen_kselftest_config.py
   ```
5. Verify unit tests:
   ```bash
   python3 -m unittest discover -s android/tests -v
   ```
6. Commit `android/configs/disabled_tests.py`, `android/configs/mandatory_tests.py` and the updated `android/vts_linux_kselftest_*.xml` files.

### 2. Adding a New Test Case

When introducing a new kselftest binary to VTS:

1. Make sure the binary is built in `Android.bp` and packaged in the `data` list of the matching `vts_linux_kselftest_<arch>` `sh_test` module for every architecture the test runs on.
2. Define the test case in `android/configs/test_definitions.py`:
   ```python
   TestCase(
       'subsystem_test_name',
       'cd &ktest_dir;/*/.; ./subsystem_test_name',
       arches=['arm_64', 'x86_64'],  # Optional, defaults to all architectures
       min_kernel_version='5.10',    # Optional
   ),
   ```
3. Classify the test in `android/configs/mandatory_tests.py`:
   ```python
   MANDATORY_TESTS = {
       ...
       'subsystem_test_name': True,   # Mandatory: must pass
       # or
       'subsystem_test_name': False,  # Skippable: exit code 4 is ignored
   }
   ```
4. Regenerate XML files:
   ```bash
   python3 android/gen_kselftest_config.py
   ```
5. Run unit tests to ensure everything is consistent:
   ```bash
   python3 -m unittest discover -s android/tests -v
   ```

### 3. Changing Mandatory / Skippable Status

To adjust whether a test is allowed to skip:

1. Edit the boolean value of the test in `android/configs/mandatory_tests.py`.
2. Regenerate XML files:
   ```bash
   python3 android/gen_kselftest_config.py
   ```
3. Verify changes using `git diff android/vts_linux_kselftest_*.xml`.

---

## Running Verification Commands

### Regenerate All Architectures
```bash
python3 android/gen_kselftest_config.py
```

### Regenerate Specific Architecture
```bash
python3 android/gen_kselftest_config.py --arch arm_64
```

### Verify Drift (CI Mode)
```bash
python3 android/gen_kselftest_config.py --check
```
Returns exit code 0 if all XML files match their configurations, or non-zero if drift is detected.

### Run Unit Tests
```bash
python3 -m unittest discover -s android/tests -v
```

In an Android tree, the same tests run as the `gen_kselftest_config_test` host test:
```bash
atest gen_kselftest_config_test
```
