/* SPDX-License-Identifier: GPL-2.0-or-later */
/*
 * Futex2 library addons for futex tests
 *
 * Copyright 2021 Collabora Ltd.
 */
#include <linux/time_types.h>
#include <stdint.h>

#define u64_to_ptr(x) ((void *)(uintptr_t)(x))

/**
 * futex_waitv - Wait at multiple futexes, wake on any
 * @waiters:    Array of waiters
 * @nr_waiters: Length of waiters array
 * @flags: Operation flags
 * @timo:  Optional timeout for operation
 */
static inline int futex_waitv(volatile struct futex_waitv *waiters, unsigned long nr_waiters,
			      unsigned long flags, struct timespec *timo, clockid_t clockid)
{
		struct __kernel_timespec ts = {
			.tv_sec = timo->tv_sec,
			.tv_nsec = timo->tv_nsec,
		};

		return syscall(__NR_futex_waitv, waiters, nr_waiters, flags, &ts, clockid);
}
