# T1 M2 Risk Candidate Review

**Status:** `AI_PROPOSAL_NOT_GOLD`

**Scope:** 9 T1 documents, 1,494 role-specific packet rows, 340 clean-clause spans checked against raw text

**Decision requested:** Independent review and adjudication by `DucAnh_N2`, `argon`, and `Minh_N1`

## What this review contains

This note lists preliminary positive-risk candidates by clause ID. It contains no contract excerpts or personal data. The working packet and source documents remain in the Data repository's ignored `data/intake/private/` area. Review each candidate against the locally available source clause before accepting, changing, or rejecting it.

The candidate packet preserves all 1,494 original rows. Seven single-unit rows are marked `RISK_CANDIDATE_NEEDS_REVIEW`; all other rows remain `UNREVIEWED` / `NEEDS_REVIEW`. Four additional proposals span multiple fragmented rows and therefore remain grouped proposals rather than row-level labels. No reviewer or adjudicator decision has been entered, and no Gold was generated.

## Proposed candidates

| Candidate clause/unit IDs | Proposed risk label | Basis | Citation candidate | Review note |
|---|---|---|---|---|
| `HDLD005_C036::EMPLOYEE`; `HDLD006_C094::EMPLOYEE`; `HDLD013_C009::EMPLOYEE` | `TERMINATION_GROUNDS_NOTICE` | `AMBIGUOUS` | Not in current Tier 1 | Employer termination right is triggered by an unspecified employee-obligation breach. HDLD005/006 are the same template wording, so they are correlated examples. Verify OCR and statutory context for HDLD013. |
| `HDLD012_C025::EMPLOYEE` | `PENALTY_DEDUCTION_DAMAGES` | `AMBIGUOUS` | Not in current Tier 1 | Liability appears to include damage to company reputation/image without criteria or limits in the clause. Review incorporated rules and statutory basis. |
| `HDLD011_C102`–`C107::EMPLOYEE` (six packet units) | `TRAINING_COMMITMENT` | `UNFAVORABLE` | Not in current Tier 1 | Bilingual/OCR passage links leaving before term end without director approval to repayment of all training costs. Read the merged source passage before deciding a row-level mapping. |
| `HDLD012_C005::EMPLOYEE`; `HDLD012_C006::EMPLOYEE` | `WORKING_HOURS_OVERTIME` | `AMBIGUOUS` | `BLLD2019:art21:cl1:ptg` | Working hours are delegated to internal rules; a related clause allows flexible shifts based on company or department needs. Verify whether the rules are attached and incorporated. |
| `HDLD012_C016::EMPLOYEE` | `BONUS_BENEFITS` | `AMBIGUOUS` | `BLLD2019:art21:cl1:ptđ` | Support payments are delegated to company rules without amount/version in the clause. Verify whether this is an agreed wage supplement and whether the rules are incorporated. |
| `HDLD011_C048`–`C049::EMPLOYEE` (two packet units) | `UNILATERAL_CHANGE` | `AMBIGUOUS` | `BLLD2019:art21:cl1:ptc` | Job description is delegated to the company charter. Check whether that document fixes the job duties sufficiently. |
| `HDLD011_C077`–`C078::EMPLOYEE` (two packet units) | `BONUS_BENEFITS` | `AMBIGUOUS` | `BLLD2019:art21:cl1:ptđ` | Other allowances are delegated to company rules without amount/version. Verify incorporation and whether the allowance is part of agreed compensation. |
| `HDLD011_C111`–`C113::EMPLOYEE` (three packet units) | `PENALTY_DEDUCTION_DAMAGES` | `AMBIGUOUS` | Not in current Tier 1 | Material liability for discipline is delegated to internal rules without criteria in the clause. Review the incorporated rules and legal basis. |

## Context item; not a positive proposal

`HDLD012_C004::EMPLOYEE` is held for context review only. Its workplace field may appear blank because of de-identification, and the travel/training assignment language may describe temporary travel rather than a contract change. Do not classify it until the original source and any annexes are checked.

## Dataset and citation limits

- The packet has 1,494 role-specific rows: 747 clause units × 2 roles. The current proposal marks seven individual rows; 13 additional packet rows are referenced in four grouped cases.
- All 340 clean T1 clauses have exact raw-text slices in the local validation. Packet source hashes use raw text for HDLD005 and HDLD007–013, and NFC-normalized raw text for HDLD006.
- Three distinct Tier 1 citations above are relevance candidates, not legal conclusions. Five of the 11 cases have a Tier 1 citation candidate. The remaining cases require legal provisions outside the 16-provision Tier 1 corpus or further source review. No citation has been invented.
- These are a preliminary shortlist, not an exhaustive finding that unlisted clauses are risk-free. Remaining packet rows stay unreviewed.

## Reviewer decision record

| Role | Reviewer ID | Decision | Date | Notes |
|---|---|---|---|---|
| Owner / annotator | `DucAnh_N2` | Pending | | |
| Reviewer | `argon` | Pending | | |
| Adjudicator | `Minh_N1` | Pending | | |

Do not convert this proposal note into M2 Gold until the three independent decisions and the disputed grouped-unit mapping are recorded in the private review packet.
