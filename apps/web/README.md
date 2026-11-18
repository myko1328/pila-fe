# Pila Web

The Next.js application for Pila, a service-discovery and virtual-queue platform for walk-in businesses.

## Requirements

- Node.js 24 or newer
- pnpm 11 or newer

## Run locally

```bash
pnpm install
pnpm dev
```

Open <http://localhost:3000>.

## Available pages

- `/` - Initial Pila product page
- `/roadmap` - Public sprint and feature implementation checklist

## Roadmap source

The canonical sprint plan is stored at:

```text
../../docs/PILA_SPRINT_BLUEPRINT.md
```

The application generates typed roadmap data from that document before development and production builds. After changing the blueprint manually, regenerate it with:

```bash
pnpm roadmap:sync
```

Feature completion states are maintained in:

```text
src/data/roadmap-progress.ts
```

Use `done`, `in-progress`, or `planned`. Viewers can see the checklist but cannot alter the authoritative project status.

## Verification

```bash
pnpm lint
pnpm build
```

## Cloudflare Workers deployment

The OpenNext adapter and Wrangler configuration are committed so Cloudflare does not need to mutate the workspace during automatic framework detection.

Use these Workers Builds settings:

```text
Root directory: apps/web
Build command: None
Deploy command: pnpm deploy
```

Do not use `npx wrangler deploy` as the deploy command for this monorepo. The `deploy` package script builds the OpenNext Worker first and then deploys the generated output.

To create the Worker bundle without deploying:

```bash
pnpm cf:build
```
