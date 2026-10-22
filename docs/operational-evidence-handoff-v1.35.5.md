# Operational Evidence Handoff — v1.35.5

The v1.35.5 handoff retains the candidate-bound portable operator kit from v1.35.4 and adds an explicit exit-plan consumer on the authoritative side. External execution still cannot approve promotion or publish releases.

## External operator responsibility

1. verify the whole operator-kit ZIP digest from the authoritative distribution;
2. verify the internal kit manifest;
3. run candidate-bound environment preflight;
4. complete one real supported-host lifecycle;
5. record real usage on both `canonical` and `package` channels;
6. meet the burn-in minimums (4 sessions, 2/channel, 24-hour window);
7. collect the allowlisted evidence ZIP and return it to the authoritative repository.

## Authoritative responsibility

Import the bundle fail-closed, rebuild live validation and promotion, request explicit approval only when `READY_FOR_APPROVAL`, then perform signed immutable release closure.

See `docs/v2-exit-plan-v1.35.5.md` for the current machine-generated next action.
