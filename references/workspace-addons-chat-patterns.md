# Workspace Add-ons & Chat Engineering Patterns

Supports `skills/14-workspace-addons-chat-engineering/SKILL.md`.

## 1. Host Adapter

```text
Gmail/Calendar/Drive/Chat event
↓
Host-specific event mapper
↓
Plain application context
↓
Application service
↓
Card/Chat renderer
```

## 2. Card Rendering

```javascript
function buildSummaryCard_(model) {
  const section = CardService.newCardSection()
    .addWidget(
      CardService.newTextParagraph()
        .setText(model.summary)
    );

  return CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle(model.title)
    )
    .addSection(section)
    .build();
}
```

## 3. Builder Order

```text
finish widget
↓
add widget to section
↓
finish section
↓
add section to card
↓
build card
```

## 4. Action Boundary

```text
card action parameter
↓
parse identifier
↓
load canonical record
↓
authorize
↓
validate transition
↓
mutate
↓
render result
```

## 5. Context Separation

```text
Homepage
= context-independent

Gmail message trigger
= message context

Drive selection trigger
= selected-item context
```

## 6. Manifest Trigger Review

```text
manifest trigger
↓
callback exists?
↓
event mapper exists?
↓
required scope?
↓
host test?
```

## 7. Card Navigation

```text
Home
→ push Detail
→ push Edit
→ pop Detail
→ pop Home
```

## 8. Async Chat / Long Work

```text
Chat event
↓
acknowledge
↓
bounded workflow / external agent
↓
Chat API progress/final update
```

## 9. Managed Agent Shell

```text
Google Chat / Workspace add-on
↓
Apps Script
↓
Vertex AI Agent Engine / remote agent
↓
tools / Workspace APIs
```

## 10. Multi-Host Capability Matrix

```markdown
| Capability | Gmail | Calendar | Drive | Chat |
|---|---:|---:|---:|---:|
| Home | yes | yes | yes | host-specific |
| Context record | message | event | items | conversation |
| Mutation | draft/label | update | metadata/action | message/action |
```

## 11. A2UI Watch Boundary

```text
A2UI
= adaptive agent-generated UI

Current status
= Early Stage Public Preview

Decision
= watch / prototype, not ordinary card baseline
```

## 12. Release Test Matrix

```text
manifest
+ homepage
+ context trigger
+ action
+ authorization
+ host rendering
+ test deployment
```

# Workspace Studio Starter Pattern — v1.21.0

```text
external event
↓
starter registration
↓
triggerId + notifyUri
↓
triggers.fire(requestId)
↓
Workspace Studio flow
```

Lifecycle:

```text
enable → triggerCreation
disable/delete → triggerDeletion
re-enable → NEW registration
```
