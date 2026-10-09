# Sections 21–30 — Deterministic Rebuild vs Incremental Update to Prevent Cache Stampede Where It Matters



Generated from `skills/06-performance-engineering/SKILL.md`.



# 21. Deterministic Rebuild vs Incremental Update

A rebuild can be easier to reason about:

```text
source
↓
view model
↓
render generated area
```

but a full rebuild may cost more than a sparse update.

Use rebuild when:

- generated layout is small/moderate,
- incremental repair is fragile,
- correctness matters more than minimal writes.

Use incremental update when:

- only a small predictable region changes,
- change detection is reliable,
- the performance difference is measurable.

Measure both before choosing.

---

# 22. Formula Cost Is Part of Workflow Cost

Apps Script can trigger expensive spreadsheet recalculation indirectly by writing values/formulas.

Performance engineering should consider:

- number of formulas,
- volatile/repeated lookups,
- large dependency chains,
- repeated formula insertion,
- cross-spreadsheet imports.

Google's best-practices guidance specifically calls out performance issues around large datasets, lookup patterns, and heavy `IMPORTRANGE` usage.

Do not profile Apps Script in isolation from the spreadsheet calculation model.

---

# 23. Batch Formula Writes

If many formulas must be installed, build a formula matrix and call `setFormulas()` or `setFormulasR1C1()` once.

Avoid one `setFormula()` call per row.

For formulas with relative references, R1C1 notation can make bulk generation clearer.

---

# 24. Consider Moving Large Repeated Lookups Into Memory

If a sheet repeatedly performs expensive lookups over a dataset already loaded by GAS, consider computing the lookup once in JavaScript.

This is especially useful for generated reports/read models.

Do not automatically replace formulas that users need to inspect/edit.

The ownership of a calculation remains an architecture decision.

---

# 25. Cache Expensive Stable Reads

`CacheService` is designed for short-term storage of results that are expensive to fetch or compute.

Candidates include:

- external API reference data,
- rarely changing lookup tables,
- expensive metadata,
- repeated configuration projections.

Pattern:

```javascript
function getReferenceData_() {
  const cache = CacheService.getScriptCache();
  const key = 'reference-data-v1';

  const cached = cache.get(key);
  if (cached !== null) {
    return JSON.parse(cached);
  }

  const value = loadReferenceData_();

  cache.put(key, JSON.stringify(value), 600);

  return value;
}
```

---

# 26. Cache Is Opportunistic

Official Apps Script documentation states cached data is **not guaranteed** to remain until its expiration time.

Every cache read must tolerate:

```javascript
null
```

Therefore:

```text
cache hit → fast path
cache miss → authoritative source
```

Never make CacheService the only copy of required business data.

---

# 27. Know Cache Limits

Current Apps Script Cache documentation states:

- key length up to 250 characters,
- value size up to 100 KB,
- up to 1,000 items in a cache.

These limits can change.

Always verify current official documentation before designing near the boundary.

Large datasets should not be forced into CacheService.

---

# 28. Choose Cache Scope Correctly

Apps Script provides:

- script cache,
- document cache,
- user cache.

Use the narrowest scope that matches the data.

Examples:

## Script cache

Shared reference data.

## User cache

User-specific preferences or recent results.

## Document cache

Document-specific derived data when running in a container context.

Do not cache user-sensitive results in a shared script cache.

Security implications belong in `07-security-engineering`.

---

# 29. Cache Invalidation Must Be Defined

Caching creates a consistency trade-off.

Define:

- cache key,
- version,
- TTL,
- invalidation event,
- authoritative fallback.

Versioned key example:

```text
customer-lookup:v3
```

A new schema can use a new key rather than reading incompatible cached JSON.

---

# 30. Prevent Cache Stampede Where It Matters

If many executions can miss the same expensive cache simultaneously:

```text
cache miss
cache miss
cache miss
     ↓
three expensive loads
```

A narrow `LockService` critical section can reduce duplication:

```javascript
function getCachedReference_() {
  const cache = CacheService.getScriptCache();
  const key = 'ref:v1';

  const first = cache.get(key);
  if (first !== null) return JSON.parse(first);

  const lock = LockService.getScriptLock();
  lock.waitLock(5000);

  try {
    const second = cache.get(key);
    if (second !== null) return JSON.parse(second);

    const value = loadExpensiveReference_();
    cache.put(key, JSON.stringify(value), 600);
    return value;
  } finally {
    lock.releaseLock();
  }
}
```

Recheck the cache after acquiring the lock.

---
