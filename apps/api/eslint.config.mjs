import js from "@eslint/js";
import eslintConfigPrettier from "eslint-config-prettier";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";

import {
  sharedIgnores,
  sharedTypeScriptRules,
} from "../../packages/configuration/eslint.shared.mjs";

const eslintConfig = defineConfig([
  globalIgnores(sharedIgnores),
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["src/**/*.ts"],
    languageOptions: {
      globals: globals.node,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      ...sharedTypeScriptRules,
      "no-console": "off",
    },
  },
  eslintConfigPrettier,
]);

export default eslintConfig;
