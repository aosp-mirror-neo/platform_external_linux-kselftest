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

"""Defines whether a kselftest is mandatory or skippable in VTS.

- True (Mandatory): The test is strictly required. It must pass on all
  devices claiming compliance. It runs in a KernelTargetTest block WITHOUT
  an exit-code-skip option, so any non-zero exit code (including exit code 4 /
  KSFT_SKIP) is treated as a hard FAILURE by Tradefed.
- False (Skippable): The test depends on specific hardware features or kernel
  configurations (e.g. CPU hotplug, hardware RTC alarm, pKVM, USERFAULTFD).
  It runs in a KernelTargetTest block WITH exit-code-skip set to 4 (KSFT_SKIP),
  so if the platform returns exit code 4, Tradefed reports it as IGNORED/SKIPPED
  instead of failing the test suite.

Every enabled test in test_definitions.ALL_TEST_CASES must be listed here.
Tests listed in disabled_tests.DISABLED_TESTS must NOT be listed here; add
the test back with its classification when it is re-enabled.
"""

MANDATORY_TESTS = {
    # Core kernel & POSIX features (Mandatory)
    'binderfs': True,
    'capabilities_test_execve': True,
    'futex_functional_run.sh': True,
    'kcmp_kcmp_test': True,
    'net_psock_tpacket': True,
    'net_reuseaddr_conflict': True,
    'net_reuseport_dualstack': True,
    'net_socket': True,
    'ptrace_peeksiginfo': True,
    'size_get_size': True,
    'splice_default_file_splice_read.sh': True,
    'timers_nanosleep': True,
    'timers_posix_timers': True,
    'timers_raw_skew': True,
    'vDSO_kselftest_vdso_test_abi': True,
    'vDSO_kselftest_vdso_test_gettimeofday': True,
    'mm_mremap_dontunmap': True,
    'mm_mremap_test': True,
    'memfd_test': True,

    # x86-specific tests (Mandatory on x86)
    'x86_single_step_syscall': True,
    'x86_sysret_ss_attrs': True,
    'x86_syscall_nt': True,
    'x86_ptrace_syscall': True,
    'x86_test_mremap_vdso': True,
    'x86_check_initial_reg_state': True,
    'x86_ldt_gdt': True,
    'x86_syscall_arg_fault': True,
    'x86_test_syscall_vdso': True,
    'x86_unwind_vdso': True,
    'x86_test_FCMOV': True,
    'x86_test_FCOMI': True,
    'x86_test_FISTTP': True,
    'x86_vdso_restorer': True,

    # Hardware-dependent / kernel-config-dependent tests (Skippable)
    'breakpoints_breakpoint_test_arm64': False,  # Requires hardware debug breakpoint registers
    'cpu_hotplug_cpu_on_off_test': False,        # Requires CONFIG_HOTPLUG_CPU and offline support
    'kvm_pvm_wipe_mem': False,                   # Requires pKVM hypervisor support
    'rtc_rtctest': False,                        # Requires hardware RTC device (/dev/rtc0) with alarms
    'mm_uffd_unit_tests': False,                 # Requires CONFIG_USERFAULTFD
    'seccomp_bpf': False,                        # seccomp-bpf filter tracing / TS_COMPAT
    'timers_inconsistency_check': False,         # Susceptible to CPU frequency scaling / virtualization
    'timers_nsleep_lat': False,                  # Latency-sensitive benchmark test
    'timers_set_tai': False,                     # Requires TAI clock offset support and permissions
    'timers_set_timer_lat': False,               # Latency-sensitive timer benchmark
    'timers_threadtest': False,                  # High-concurrency thread timer stress test
    'timers_valid_adjtimex': False,              # Requires adjtimex tick rate adjustment support
    'vDSO_kselftest_vdso_test_getcpu': False,    # __vdso_getcpu is unsupported on ARM64; returns KSFT_SKIP (4)
}
