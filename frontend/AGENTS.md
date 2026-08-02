# Frontend guidance

- The websocket state is the frontend contract. Regenerate `src/schemas/types.gen.ts` with `npm run generate:schema` after backend OpenAPI changes; do not hand-maintain generated types.
- `delegations` is a dictionary keyed by representation ID. Use `Object.values()` only for display lists and resolve queue/speaker IDs through the dictionary.
- Seat labels are opaque layout keys. Render maps by direct seat lookup, not by sorted delegation position or array index.
- Do not mutate Zustand-selected state during render (for example, sorting it in place).
- Run `npm run build` after frontend changes; identify unrelated baseline failures rather than hiding them.
