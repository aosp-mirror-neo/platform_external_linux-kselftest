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

"""Test case definitions and command metadata for kselftest."""

from typing import List, Optional


class TestCase:
    """Represents a kselftest test case in VTS."""

    def __init__(
        self,
        base_name: str,
        command: str,
        arches: Optional[List[str]] = None,
        min_kernel_version: Optional[str] = None,
    ):
        self.base_name = base_name
        self.command = command
        # None indicates support for all architectures.
        self.arches = arches
        self.min_kernel_version = min_kernel_version

    def is_supported_on(self, arch: str) -> bool:
        if self.arches is None:
            return True
        return arch in self.arches


ALL_TEST_CASES = [
    TestCase(
        'binderfs',
        'cd &ktest_dir;/*/.; ./binderfs_test',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'breakpoints_breakpoint_test_arm64',
        'cd &ktest_dir;/*/.; ./breakpoint_test',
        arches=['arm_64'],
    ),
    TestCase(
        'capabilities_test_execve',
        'cd &ktest_dir;/*/.; ./test_execve',
    ),
    TestCase(
        'cpu_hotplug_cpu_on_off_test',
        # cpu-on-off-test.sh checks $UID, which bash sets but Android's mksh
        # does not (b/484821521). Set it on every architecture until the
        # upstream fix "selftests/cpu-hotplug: Use $(id -u) instead of $UID
        # for root check" is imported, then drop the UID= prefix.
        'cd &ktest_dir;/*/.; UID=$(id -u) ./cpu-on-off-test.sh',
    ),
    TestCase(
        'futex_functional_run.sh',
        'cd &ktest_dir;/*/.; USE_COLOR=0 ./run.sh',
        # run.sh and the futex binaries are not packaged for riscv_64.
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
        min_kernel_version='5.1',
    ),
    TestCase(
        'kcmp_kcmp_test',
        'cd &ktest_dir;/*/.; ./kcmp_test',
    ),
    TestCase(
        'kvm_pvm_wipe_mem',
        'cd &ktest_dir;/*/.; ./pvm_wipe_mem',
        arches=['arm_64'],
    ),
    TestCase(
        'net_psock_tpacket',
        'cd &ktest_dir;/*/.; ./psock_tpacket',
        arches=['arm_64', 'x86_64', 'riscv_64'],
    ),
    TestCase(
        'net_reuseaddr_conflict',
        'cd &ktest_dir;/*/.; ./reuseaddr_conflict',
    ),
    TestCase(
        'net_reuseport_dualstack',
        'cd &ktest_dir;/*/.; ./reuseport_dualstack',
    ),
    TestCase(
        'net_socket',
        'cd &ktest_dir;/*/.; ./socket',
    ),
    TestCase(
        'net_test_bpf',
        'cd &ktest_dir;/*/.; ./test_bpf.sh',
    ),
    TestCase(
        'net_psock_fanout',
        'cd &ktest_dir;/*/.; ./psock_fanout',
    ),
    TestCase(
        'ptrace_peeksiginfo',
        'cd &ktest_dir;/*/.; ./peeksiginfo',
        arches=['arm_64', 'x86_64', 'riscv_64'],
    ),
    TestCase(
        'rtc_rtctest',
        'cd &ktest_dir;/*/.; ./rtctest',
    ),
    TestCase(
        'size_get_size',
        'cd &ktest_dir;/*/.; ./get_size',
    ),
    TestCase(
        'splice_default_file_splice_read.sh',
        'cd &ktest_dir;/*/.; ./default_file_splice_read.sh',
    ),
    TestCase(
        'timers_inconsistency_check',
        'cd &ktest_dir;/*/.; ./inconsistency-check',
    ),
    TestCase(
        'timers_nanosleep',
        'cd &ktest_dir;/*/.; ./nanosleep',
    ),
    TestCase(
        'timers_nsleep_lat',
        'cd &ktest_dir;/*/.; ./nsleep-lat',
    ),
    TestCase(
        'timers_posix_timers',
        'cd &ktest_dir;/*/.; ./posix_timers',
    ),
    TestCase(
        'timers_raw_skew',
        'cd &ktest_dir;/*/.; ./raw_skew 30',
    ),
    TestCase(
        'timers_set_tai',
        'cd &ktest_dir;/*/.; ./set-tai',
    ),
    TestCase(
        'timers_set_timer_lat',
        'cd &ktest_dir;/*/.; ./set-timer-lat',
    ),
    TestCase(
        'timers_threadtest',
        'cd &ktest_dir;/*/.; ./threadtest',
    ),
    TestCase(
        'timers_valid_adjtimex',
        'cd &ktest_dir;/*/.; ./valid-adjtimex',
    ),
    TestCase(
        'timers_adjtick',
        'cd &ktest_dir;/*/.; ./adjtick',
    ),
    TestCase(
        'timers_alarmtimer_suspend',
        'cd &ktest_dir;/*/.; ./alarmtimer-suspend',
    ),
    TestCase(
        'timers_clocksource_switch',
        'cd &ktest_dir;/*/.; ./clocksource-switch',
    ),
    TestCase(
        'timers_freq_step',
        'cd &ktest_dir;/*/.; ./freq-step',
    ),
    TestCase(
        'timers_leap_a_day',
        'cd &ktest_dir;/*/.; ./leap-a-day',
    ),
    TestCase(
        'timers_leapcrash',
        'cd &ktest_dir;/*/.; ./leapcrash',
    ),
    TestCase(
        'timers_set_2038',
        'cd &ktest_dir;/*/.; ./set-2038',
    ),
    TestCase(
        'timers_set_tz',
        'cd &ktest_dir;/*/.; ./set-tz',
    ),
    TestCase(
        'timers_skew_consistency',
        'cd &ktest_dir;/*/.; ./skew_consistency',
    ),
    TestCase(
        'timers_change_skew',
        'cd &ktest_dir;/*/.; ./change_skew',
    ),
    TestCase(
        'vDSO_kselftest_vdso_test_abi',
        'cd &ktest_dir;/*/.; ./kselftest_vdso_test_abi',
        arches=['arm_64', 'x86_64', 'riscv_64'],
    ),
    TestCase(
        'vDSO_kselftest_vdso_test_getcpu',
        'cd &ktest_dir;/*/.; ./kselftest_vdso_test_getcpu',
        arches=['arm_64', 'x86_64', 'riscv_64'],
    ),
    TestCase(
        'vDSO_kselftest_vdso_test_gettimeofday',
        'cd &ktest_dir;/*/.; ./kselftest_vdso_test_gettimeofday',
        arches=['arm_64', 'x86_64', 'riscv_64'],
    ),
    TestCase(
        'mm_mremap_dontunmap',
        'cd &ktest_dir;/*/.; ./mremap_dontunmap',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_mremap_test',
        'cd &ktest_dir;/*/.; ./mremap_test',
        arches=['arm_64', 'x86_64'],
    ),
    TestCase(
        'mm_uffd_unit_tests',
        'cd &ktest_dir;/*/.; ./uffd-unit-tests',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_compaction_test',
        'cd &ktest_dir;/*/.; ./compaction_test',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_hugetlb_mmap',
        'cd &ktest_dir;/*/.; ./hugetlb-mmap',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_hugetlb_shm',
        'cd &ktest_dir;/*/.; ./hugetlb-shm',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_mlock_random_test',
        'cd &ktest_dir;/*/.; ./mlock-random-test',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_mlock2_tests',
        'cd &ktest_dir;/*/.; ./mlock2-tests',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_on_fault_limit',
        'cd &ktest_dir;/*/.; ./on-fault-limit',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_thuge_gen',
        'cd &ktest_dir;/*/.; ./thuge-gen',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_transhuge_stress',
        'cd &ktest_dir;/*/.; ./transhuge-stress',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'mm_run_vmtests',
        'cd &ktest_dir;/*/.; ./run_vmtests.sh',
        arches=['arm_64', 'arm_32', 'x86_64', 'x86_32'],
    ),
    TestCase(
        'membarrier_test_single_thread',
        'cd &ktest_dir;/*/.; ./membarrier_test_single_thread',
    ),
    TestCase(
        'membarrier_test_multi_thread',
        'cd &ktest_dir;/*/.; ./membarrier_test_multi_thread',
    ),
    TestCase(
        'exec_test_execveat',
        'cd &ktest_dir;/*/.; ./execveat',
    ),
    TestCase(
        'memfd_test',
        'cd &ktest_dir;/*/.; ./memfd_test',
        # Tests MFD_EXEC / MFD_NOEXEC_SEAL added in 6.3 (b/582542744).
        min_kernel_version='6.6',
    ),
    TestCase(
        'seccomp_bpf',
        'cd &ktest_dir;/*/.; ./seccomp_bpf',
        # Tests user_ioctl_notification_filter_empty added in 6.11 (b/582542744).
        min_kernel_version='6.12',
    ),
    # x86-specific tests
    TestCase(
        'x86_single_step_syscall',
        'cd &ktest_dir;/*/.; ./single_step_syscall',
        arches=['x86_64', 'x86_32'],
        # Fails by design on 5.10 and older kernels (b/191663053, b/392943794).
        min_kernel_version='5.15',
    ),
    TestCase(
        'x86_sysret_ss_attrs',
        'cd &ktest_dir;/*/.; ./sysret_ss_attrs',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_syscall_nt',
        'cd &ktest_dir;/*/.; ./syscall_nt',
        arches=['x86_64', 'x86_32'],
    ),
    TestCase(
        'x86_ptrace_syscall',
        'cd &ktest_dir;/*/.; ./ptrace_syscall',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_test_mremap_vdso',
        'cd &ktest_dir;/*/.; ./test_mremap_vdso',
        arches=['x86_64', 'x86_32'],
    ),
    TestCase(
        'x86_check_initial_reg_state',
        'cd &ktest_dir;/*/.; ./check_initial_reg_state',
        arches=['x86_64', 'x86_32'],
    ),
    TestCase(
        'x86_ldt_gdt',
        'cd &ktest_dir;/*/.; ./ldt_gdt',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_syscall_arg_fault',
        'cd &ktest_dir;/*/.; ./syscall_arg_fault',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_test_syscall_vdso',
        'cd &ktest_dir;/*/.; ./test_syscall_vdso',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_unwind_vdso',
        'cd &ktest_dir;/*/.; ./unwind_vdso',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_test_FCMOV',
        'cd &ktest_dir;/*/.; ./test_FCMOV',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_test_FCOMI',
        'cd &ktest_dir;/*/.; ./test_FCOMI',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_test_FISTTP',
        'cd &ktest_dir;/*/.; ./test_FISTTP',
        arches=['x86_32'],
    ),
    TestCase(
        'x86_vdso_restorer',
        'cd &ktest_dir;/*/.; ./vdso_restorer',
        arches=['x86_32'],
    ),
]
