/*
 * Configuration for generating frontend OpenAPI types.
 */
export default {
  input: process.env.OPENAPI_URL ?? 'http://localhost:8000/openapi.json',
  output: {
    entryFile: false,
    path: 'src/schemas',
  },
  plugins: [
    {
      enums: true,
      name: '@hey-api/typescript',
    },
  ],
};
