# PRD: Implement Honcho Memory Operating Workflow

## Problem
The Honcho research exists only in chat history and one durable preference. Future agents need repository-local guidance for when and how to use Honcho efficiently, without ad hoc memory calls or conflicting conventions.

## Outcome
Add concise Honcho usage guidance to the template so agents can apply Honcho as a persistent memory/reasoning layer during normal OMP work.

## Acceptance Criteria
1. The repository contains durable Honcho guidance covering memory boundaries, tool selection, reasoning-level selection, retrieval flow, and persistence rules.
2. Guidance is discoverable from existing agent-facing template documentation.
3. Guidance preserves existing br/bv workflow rules and does not replace project artifacts as the source of truth.
4. Verification confirms the updated documentation includes the required Honcho sections.

## Non-Goals
- Do not add SDK code, MCP credentials, secrets, or runtime integration.
- Do not change br/bv workflow semantics.
- Do not create speculative automation beyond documentation/instructions.
