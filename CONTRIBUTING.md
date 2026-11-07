# Contributing to Open420

Thanks for helping build an open radio.

## Sign-off (DCO)

Every commit must be signed off, certifying the
[Developer Certificate of Origin](https://developercertificate.org):

```bash
git commit -s -m "Describe your change"
```

## Licensing

By contributing, you agree that your work is licensed under the license that
covers the folder it lives in (see `REUSE.toml`). Keep all existing copyright
notices, and add your own where you make significant changes.

New source files should start with an SPDX header, for example:

```cpp
// SPDX-FileCopyrightText: 2026 Your Name
// SPDX-License-Identifier: GPL-3.0-or-later
```

Run `reuse lint` before opening a pull request.

## Modules

Expansion modules are welcome. Start from the official module template
(coming soon) so your module carries the correct license and credits.
Verified modules are listed in the main repo; open a pull request or email
the maintainer to request verification.
