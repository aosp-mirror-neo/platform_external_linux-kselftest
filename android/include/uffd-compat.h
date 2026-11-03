/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
/*
 * Fallback userfaultfd and pagemap UAPI definitions for bionic.
 *
 * uffd-unit-tests.c uses UAPI added in v7.3 (userfaultfd RWP and
 * PAGE_IS_ACCESSED), but bionic's kernel headers are older. Include the
 * bionic headers first and only define what is missing, so this file is a
 * no-op once bionic ships the v7.3 headers.
 *
 * Values match include/uapi/linux/userfaultfd.h and
 * include/uapi/linux/fs.h in v7.3.
 *
 * TODO(b/578943197): Remove once bionic ships v7.3 kernel headers.
 */
#ifndef __ANDROID_UFFD_COMPAT_H
#define __ANDROID_UFFD_COMPAT_H

#include <linux/fs.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/userfaultfd.h>

#ifndef PAGE_IS_ACCESSED
#define PAGE_IS_ACCESSED		(1 << 9)
#endif

#ifndef UFFD_PAGEFAULT_FLAG_RWP
#define UFFD_PAGEFAULT_FLAG_RWP		(1 << 3)
#endif

#ifndef UFFD_FEATURE_RWP
#define UFFD_FEATURE_RWP		(1 << 17)
#endif

#ifndef UFFD_FEATURE_RWP_ASYNC
#define UFFD_FEATURE_RWP_ASYNC		(1 << 18)
#endif

#ifndef UFFDIO_REGISTER_MODE_RWP
#define UFFDIO_REGISTER_MODE_RWP	((__u64)1 << 3)
#endif

#ifndef UFFDIO_RWPROTECT
#define _UFFDIO_RWPROTECT		(0x09)
struct uffdio_rwprotect {
	struct uffdio_range range;
	/* !RWP means undo RWP-protection */
#define UFFDIO_RWPROTECT_MODE_RWP	((__u64)1 << 0)
#define UFFDIO_RWPROTECT_MODE_DONTWAKE	((__u64)1 << 1)
	__u64 mode;
};
#define UFFDIO_RWPROTECT		_IOWR(UFFDIO, _UFFDIO_RWPROTECT, \
					      struct uffdio_rwprotect)
#endif

#ifndef UFFDIO_SET_MODE
#define _UFFDIO_SET_MODE		(0x0A)
struct uffdio_set_mode {
	__u64 enable;
	__u64 disable;
};
#define UFFDIO_SET_MODE			_IOW(UFFDIO, _UFFDIO_SET_MODE, \
					     struct uffdio_set_mode)
#endif

#endif /* __ANDROID_UFFD_COMPAT_H */
