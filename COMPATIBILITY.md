# Compatibility Matrix

| Release | Minimum NetBox Version | Maximum NetBox Version |
|---------|------------------------|------------------------|
| 0.1.0   | 4.5.0                  | 4.6.x                  |

A single plugin release supports **both** NetBox 4.5.x and 4.6.x. CI runs
the full test suite against the latest patch of each supported NetBox
minor on every push.

When NetBox 4.7 ships, this matrix gets a new row; the 4.5/4.6 row stays
frozen so existing deployments have a clear pin target.
