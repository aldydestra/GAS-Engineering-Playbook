# Google Apps Script Core Patterns

These patterns support `skills/01-gas-core-engineering/SKILL.md`.

They are reusable examples, not a mandatory framework.

## 1. Custom Menu

```javascript
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Tools')
    .addItem('Update All', 'menuUpdateAll')
    .addSeparator()
    .addItem('Refresh Data', 'menuRefreshData')
    .addItem('Rebuild Dashboard', 'menuRebuildDashboard')
    .addToUi();
}
```

Keep menu callbacks public.

## 2. Thin Trigger

```javascript
function onEdit(e) {
  if (!e || !e.range) return;

  const sheet = e.range.getSheet();
  if (sheet.getName() !== 'Input') return;
  if (e.range.getColumn() !== 3) return;

  EditService_handle(e);
}
```

Filter early before expensive work.

## 3. Batch Read / Write

```javascript
function normalizeData() {
  const sheet = SpreadsheetApp.getActive().getSheetByName('Data');
  if (!sheet) throw new Error('Missing sheet: Data');

  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  const values = sheet.getRange(2, 1, lastRow - 1, 3).getValues();

  const output = values.map(row => [
    String(row[0]).trim(),
    String(row[1]).trim(),
    row[2]
  ]);

  sheet.getRange(2, 1, output.length, output[0].length).setValues(output);
}
```

## 4. Header Map

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, value, index) => {
    const key = String(value).trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Use semantic headers when source layouts can evolve.

## 5. Properties-backed Configuration

```javascript
function getConfig_() {
  const props = PropertiesService.getScriptProperties();

  return {
    apiBaseUrl: props.getProperty('API_BASE_URL'),
    environment: props.getProperty('ENVIRONMENT') || 'development'
  };
}
```

Do not store secrets directly in ordinary source constants.

## 6. Lock Around Shared Mutation

```javascript
function runExclusiveUpdate() {
  const lock = LockService.getScriptLock();

  if (!lock.tryLock(5000)) {
    throw new Error('Update already running.');
  }

  try {
    performUpdate_();
  } finally {
    lock.releaseLock();
  }
}
```

## 7. HTML RPC

Client:

```javascript
google.script.run
  .withSuccessHandler(result => {
    console.log(result);
  })
  .withFailureHandler(error => {
    console.error(error.message);
  })
  .saveRecord(payload);
```

Server:

```javascript
function saveRecord(payload) {
  validatePayload_(payload);
  return RecordService_save_(payload);
}
```

## 8. Installable Trigger Setup

```javascript
function installDailyTrigger() {
  ScriptApp.newTrigger('dailyRefresh')
    .timeBased()
    .atHour(8)
    .everyDays(1)
    .create();
}
```

Avoid creating duplicate triggers repeatedly; production setup routines should check existing triggers first.

## 9. External API Wrapper

```javascript
function fetchJson_(url, options = {}) {
  const response = UrlFetchApp.fetch(url, {
    ...options,
    muteHttpExceptions: true
  });

  const code = response.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error(`HTTP ${code}: ${response.getContentText()}`);
  }

  return JSON.parse(response.getContentText());
}
```

## 10. Deterministic Rebuild

```javascript
function rebuildDashboard() {
  const ss = SpreadsheetApp.getActive();
  const sheet = ss.getSheetByName('Dashboard');
  if (!sheet) throw new Error('Missing sheet: Dashboard');

  // Clear only the generated region.
  sheet.getRange('A1:H100').clearContent().clearFormat();

  const model = buildDashboardModel_();
  renderDashboard_(sheet, model);

  SpreadsheetApp.flush();
}
```

Use deterministic rebuilds for generated layouts when incremental repair becomes fragile.
