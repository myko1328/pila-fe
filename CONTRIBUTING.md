# Contributing to Pila

## Development requirements

- Node.js 22 or newer
- pnpm 11.25.0
- Install dependencies from the repository root with `pnpm install --frozen-lockfile` in CI or `pnpm install` locally.

## Before starting work

1. Confirm the target feature and acceptance criteria in `docs/PILA_SPRINT_BLUEPRINT.md`.
2. Keep frontend work in `apps/web` and backend work in `apps/api`.
3. Put framework-neutral API contracts in `packages/contracts`.
4. Do not add database or production business API work before the Phase 2 frontend sign-off gate.

## Code standards

- Use TypeScript for application code.
- Preserve strict compiler settings; do not suppress errors with `any` or `@ts-ignore` without a documented reason.
- Use `@/*` for cross-directory frontend imports and `#api/*` for cross-directory API imports.
- Keep same-directory imports relative when that makes ownership clearer.
- Use `type` imports when a symbol is used only as a type.
- Use PascalCase for types and React components, camelCase for functions and variables, and UPPER_CASE for module constants.
- Keep generated files and build output out of linting, formatting, and commits.

## Required checks

Run these commands from the repository root before requesting review:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Use `pnpm format` and `pnpm lint:fix` for safe automatic fixes.

## Commits

- Group one coherent feature or fix into each commit.
- Use an imperative Conventional Commit-style message, such as `feat: add queue health endpoint` or `fix: align Worker configuration`.
- Do not commit `.env` files, secrets, generated build output, or temporary artifacts.
