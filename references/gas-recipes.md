# GAS Core Recipes

Small reusable recipes derived from common Apps Script workflows.

## Archive Rows in Bulk

For large datasets, prefer building retained/archive arrays and writing in batches rather than repeatedly calling `appendRow()` and `deleteRow()`.

```javascript
function splitCompletedRows_(rows, statusIndex) {
  const active = [];
  const archive = [];

  rows.forEach(row => {
    (row[statusIndex] === 'Complete' ? archive : active).push(row);
  });

  return { active, archive };
}
```

## Duplicate Detection in Memory

```javascript
function findDuplicateRows_(values, keyIndex) {
  const seen = new Set();
  const duplicates = [];

  values.forEach((row, index) => {
    const key = String(row[keyIndex]).trim();
    if (!key) return;

    if (seen.has(key)) duplicates.push(index);
    else seen.add(key);
  });

  return duplicates;
}
```

Apply formatting to grouped ranges where practical rather than issuing one style call per cell.

## Batch Email With Quota Guard

```javascript
function sendPreparedEmails(items) {
  const remaining = MailApp.getRemainingDailyQuota();
  const sendable = items.filter(item => item.email && !item.sent);

  if (sendable.length > remaining) {
    throw new Error(
      `Email quota insufficient. Need ${sendable.length}, remaining ${remaining}.`
    );
  }

  sendable.forEach(item => {
    MailApp.sendEmail({
      to: item.email,
      subject: item.subject,
      htmlBody: item.htmlBody
    });
  });
}
```

For larger notification workloads, add checkpointing and idempotent send status.

## Multi-sheet Processing

```javascript
function processNamedSheets_(sheetNames) {
  const ss = SpreadsheetApp.getActive();

  for (const name of sheetNames) {
    const sheet = ss.getSheetByName(name);
    if (!sheet) {
      console.warn(`Skipping missing sheet: ${name}`);
      continue;
    }

    processSheet_(sheet);
  }
}
```

Prefer an explicit list/configuration over relying on whatever sheet is currently active.
