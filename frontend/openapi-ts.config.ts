/*
Configuração para geração automática do types.gen.ts para Schemas na frontend
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
  ]
};
