# Pila

Pila is a pnpm monorepo for a service-discovery and virtual-queue product.

## Applications

- `apps/web` — Next.js frontend deployed independently to Cloudflare Workers.
- `apps/api` — Node.js and Express REST API deployed to a Node.js runtime.
- `apps/worker` — reserved for background processing in a later sprint.

## Shared packages

- `packages/contracts` — framework-neutral request and response contracts.
- `packages/configuration` — shared repository configuration.
- `packages/testing` — shared testing utilities and conventions.

## Commands

Install all workspace dependencies from the repository root:

```bash
pnpm install
```

Run both applications:

```bash
pnpm dev
```

Run an application independently:

```bash
pnpm dev:web
pnpm dev:api
```

Validate the complete workspace:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Use `pnpm format` and `pnpm lint:fix` to apply safe automatic formatting and lint fixes. See `CONTRIBUTING.md` for repository conventions and required checks.
