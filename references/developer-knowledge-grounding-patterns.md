# Developer Knowledge Grounding Patterns

Supports:

- `skills/11-documentation-engineering/SKILL.md`
- `skills/13-ai-agent-integration/SKILL.md`
- `docs/skill-authoring-guide.md`

Google Developer Knowledge is an official Google service for searching and retrieving public developer documentation through REST and MCP.

Use it as an evidence-retrieval layer, not as a replacement for engineering judgment.

---

## 1. Evidence Retrieval Flow

```text
question / repository claim
↓
search official documentation
↓
inspect source metadata
↓
retrieve relevant source
↓
compare claim
↓
adopt / correct / watch
```

---

## 2. MCP Tool Selection

```text
search_documents
→ find relevant official docs

get_documents
→ retrieve full source documents

answer_query
→ grounded synthesis with references
```

For critical platform facts, retrieve the referenced source document.

---

## 3. REST Search

Conceptually:

```text
SearchDocumentChunks
↓
content
document.uri
document.dataSource
document.updateTime
relevanceScore
```

This is useful for automated technology-watch jobs.

---

## 4. Freshness Filter

Example concept:

```text
updateTime >= <last_audit_time>
AND
dataSource = "developers.google.com"
```

Then review only changed/relevant sources.

Do not assume every source update is semantically relevant.

---

## 5. Exact URI Verification

For a known release-note page:

```text
filter by uri
↓
retrieve current source
↓
compare latest entry/date
```

This is stronger than a broad web result when exact freshness matters.

---

## 6. Synthesis vs Source

```text
answer_query
= discovery/synthesis

underlying document
= normative evidence
```

Do not quote a synthesized answer as if it were the original Google specification.

---

## 7. Quota Fallback

If grounded-answer quota is exhausted:

```text
answer_query → 429
↓
search_documents
↓
get_documents
↓
manual/application synthesis
```

The service's official MCP guidance explicitly supports a search fallback.

---

## 8. Data Source Boundary

Current corpus includes public Google developer domains such as:

```text
developers.google.com
ai.google.dev
cloud.google.com
docs.cloud.google.com
adk.dev
geminicli.com
```

Do not expect it to retrieve:

- private project docs;
- GitHub third-party repositories;
- user-uploaded files;
- internal organization docs.

Use the appropriate source connector/review path.

---

## 9. Re-Index Freshness

The corpus states a goal of indexing updated documentation within roughly two business days.

Therefore:

```text
normal periodic audit
→ Developer Knowledge is appropriate

breaking same-day change
→ direct release-note/source verification may still be required
```

---

## 10. Grounding for Agent Tool Use

```text
agent needs current API fact
↓
official-doc grounding tool
↓
retrieve answer/source
↓
application validates tool policy
↓
execute allowed action
```

Documentation grounding does not grant execution authority.

---

## 11. Source Metadata Record

For important repository updates, store:

```text
source URI
source class
update time
audit date
affected skill
adoption decision
```

This makes later corrections traceable.

---

## 12. Technology Watch Automation

Possible future workflow:

```text
scheduled check
↓
search docs changed since last audit
↓
classify by relevant product/domain
↓
create candidate findings
↓
human/agent review
↓
ADOPT / WATCH / NO ACTION
```

Do not automatically rewrite skills from every search result.

---

## 13. Error Handling

Current service guidance distinguishes failures such as:

```text
401 unauthenticated
403 permission/configuration
404 resource missing
429 quota/rate limit
503 unavailable
504 deadline exceeded
```

Retry only transient categories.

Use bounded exponential backoff with jitter where the service guidance recommends it.

---

## 14. MCP Timeout

Current Developer Knowledge MCP guidance recommends host-side tool timeout handling because remote tool calls can exceed a short client deadline.

This is a **Developer Knowledge MCP client** concern.

Do not confuse it with Apps Script `UrlFetchApp.timeoutSeconds`; each boundary has its own timeout configuration.

---

## 15. Release Audit Template

```markdown
## Source

URI:
Data source:
Source update time:
Audit date:

## Existing Claim

...

## Retrieved Evidence

...

## Decision

ADOPT / CORRECT / WATCH / NO ACTION

## Affected Skills

- ...

## Verification Needed

...
```

---

# Official References

- Developer Knowledge release notes  
  https://developers.google.com/knowledge/release-notes

- Connect to Developer Knowledge MCP  
  https://developers.google.com/knowledge/mcp

- MCP reference  
  https://developers.google.com/knowledge/reference/mcp

- Search and retrieve documents  
  https://developers.google.com/knowledge/howto

- Corpus reference  
  https://developers.google.com/knowledge/reference/corpus-reference

- AnswerQuery  
  https://developers.google.com/knowledge/reference/rest/v1/TopLevel/answerQuery

- Error handling and quotas  
  https://developers.google.com/knowledge/error-handling-and-limits

# Developer Knowledge CLI GA — v1.22.0

Current GA gcloud commands include:

```text
gcloud developer-knowledge answer-query
gcloud developer-knowledge documents describe
gcloud developer-knowledge documents search-chunks
```

Use:

```text
answer-query
→ grounded synthesized answer

search-chunks
→ raw relevant documentation chunks

documents describe
→ source metadata/content
```

Preserve source URI, update time, citations/references, and retrieval context where they materially support the final answer.

A relevance score is a retrieval-ranking signal, not a truth score.
