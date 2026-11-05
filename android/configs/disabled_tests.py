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

"""Tests that are completely disabled in Android VTS (excluded from XML).

Add test base names here along with a bug reference (e.g. 'b/12345678')
to exclude them from the generated Tradefed test XML configurations.
A disabled test must not also be listed in mandatory_tests.MANDATORY_TESTS.
"""

DISABLED_TESTS = {
    # Tests that cannot pass on Android GKI kernels
    'net_test_bpf': 'b/564344583: test_bpf.sh loads the test_bpf module (CONFIG_TEST_BPF), which GKI does not ship',
    'net_psock_fanout': 'b/564344583: Disabled in ACK BUILD.bazel due to test failures',

    # Dangerous timers that interfere with system state or stability
    'timers_alarmtimer_suspend': 'b/564344583: Attempts device suspend (PM_SUSPEND_MEM); breaks virtual devices/CI',
    'timers_clocksource_switch': 'b/564344583: Requires root and changes system clocksource',
    'timers_set_2038': 'b/564344583: Sets RTC to 2038; breaks system TLS certificates and Keystore',
    'timers_set_tz': 'b/564344583: Modifies system timezone setting',
    'timers_leap_a_day': 'b/564344583: Long-running leap second stress test; unsuitable for CI',
    'timers_leapcrash': 'b/564344583: Modifies leap second flags; unsuitable for CI',

    # Timers built in Android.bp but not packaged in sh_test data
    'timers_adjtick': 'b/564344583: Excluded from VTS sh_test data',
    'timers_freq_step': 'b/564344583: Excluded from VTS sh_test data',
    'timers_skew_consistency': 'b/564344583: Excluded from VTS sh_test data',
    'timers_change_skew': 'b/564344583: Excluded from VTS sh_test data',

    # Hugepage / Hugetlbfs tests (unsupported on Android mobile devices)
    'mm_hugetlb_mmap': 'b/564344583: Android devices do not configure hugetlbfs (/dev/hugepages)',
    'mm_hugetlb_shm': 'b/564344583: Android devices do not configure hugetlbfs (/dev/hugepages)',
    'mm_thuge_gen': 'b/564344583: Android devices do not configure hugetlbfs (/dev/hugepages)',
    'mm_transhuge_stress': 'b/564344583: Android devices do not configure hugetlbfs (/dev/hugepages)',
    'mm_compaction_test': 'b/564344583: Excluded from VTS in ACK; requires memory compaction setup',
    'mm_mlock_random_test': 'b/564344583: Excluded from VTS in ACK; requires unprivileged mlock rlimits',
    'mm_mlock2_tests': 'b/564344583: Excluded from VTS in ACK; requires unprivileged mlock rlimits',
    'mm_on_fault_limit': 'b/564344583: Excluded from VTS in ACK',
    'mm_run_vmtests': 'b/564344583: Excluded from VTS; composite test runner',

    # Tests pending sh_test data inclusion
    'membarrier_test_single_thread': 'b/564344583: Pending inclusion in sh_test data',
    'membarrier_test_multi_thread': 'b/564344583: Pending inclusion in sh_test data',
    'exec_test_execveat': 'b/564344583: Pending inclusion in sh_test data',
}
