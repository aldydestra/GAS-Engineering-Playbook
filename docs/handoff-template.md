# Engineering Handoff Template

Use this as a compact safety net when work must continue in another session or by another maintainer.

Do not include credentials, private keys, personal data, or sensitive production endpoints.

## Project / Workstream

- Name:
- Repository:
- Current repository version:
- Current branch/commit:
- Date:

## Current Objective

What is being built, fixed, migrated, or investigated?

## Confirmed Current State

- ...

Only include verified facts.

## Completed

- ...

## In Progress

- ...

## Pending / Next Recommended Steps

1. ...
2. ...

## Known Issues

| Issue | Evidence | Impact | Current workaround |
|---|---|---|---|
| | | | |

## Hypotheses / Unverified

- ...

Keep hypotheses separate from confirmed facts.

## Architecture / Important Contracts

- source of truth:
- stable IDs:
- public entry points:
- deployment model:
- trigger ownership:
- database/API boundary:

## Relevant Files

- `...`
- `...`

## Configuration

Document property **names and purpose**, not secret values.

| Property | Purpose | Environment |
|---|---|---|
| | | |

## Test / Verification Status

- unit:
- integration:
- live GAS:
- manual:
- known gaps:

## Operational State

- current production GAS version:
- previous known-good version:
- latest successful job:
- open incident:

Use private operational records for sensitive IDs.

## Recent Decisions

- ...

Link ADRs where available.

## Recent Release / Changelog

- repository release:
- primary changes:
- compatibility notes:

## Sources / Evidence

### Official documentation

- ...

### Project experience

- ...

### Community / external references

- ...

## Safety Notes

- secrets that must never be committed:
- destructive operations to avoid:
- production resources that require approval:

## Handoff Summary

One compact paragraph describing exactly where the next maintainer should resume.
