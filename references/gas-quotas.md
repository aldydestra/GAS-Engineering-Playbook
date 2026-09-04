# GAS Quota-Aware Engineering

Treat quotas as current platform configuration, not permanent constants.

Always verify:

https://developers.google.com/apps-script/guides/services/quotas

Design response:

1. reduce service calls,
2. batch,
3. cache,
4. chunk,
5. checkpoint,
6. continue,
7. make retry safe.
