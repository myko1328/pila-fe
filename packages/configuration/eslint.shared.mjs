export const sharedIgnores = [
  "node_modules/**",
  "dist/**",
  "build/**",
  "coverage/**",
  "*.tsbuildinfo",
];

export const sharedTypeScriptRules = {
  "no-duplicate-imports": "error",
  "sort-imports": [
    "error",
    {
      allowSeparatedGroups: true,
      ignoreCase: false,
      ignoreDeclarationSort: true,
      ignoreMemberSort: false,
      memberSyntaxSortOrder: ["none", "all", "multiple", "single"],
    },
  ],
  "@typescript-eslint/consistent-type-imports": [
    "error",
    {
      fixStyle: "inline-type-imports",
      prefer: "type-imports",
    },
  ],
  "@typescript-eslint/no-import-type-side-effects": "error",
};
