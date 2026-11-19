# @pila/configuration

Shared TypeScript, linting, formatting, and other repository configuration.

Applications extend the strict TypeScript baseline with:

```json
{
  "extends": "../../packages/configuration/tsconfig.base.json"
}
```

Application ESLint configurations also compose `eslint.shared.mjs` for common import and type-import rules while retaining framework-specific rules.
