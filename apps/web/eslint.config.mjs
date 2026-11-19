import { defineConfig, globalIgnores } from "eslint/config";
import eslintConfigPrettier from "eslint-config-prettier";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

import {
  sharedIgnores,
  sharedTypeScriptRules,
} from "../../packages/configuration/eslint.shared.mjs";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    ".open-next/**",
    ".wrangler/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    ...sharedIgnores,
  ]),
  {
    rules: sharedTypeScriptRules,
  },
  eslintConfigPrettier,
]);

export default eslintConfig;
