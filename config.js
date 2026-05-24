// Hemingway configuration.
//
// When you stand up your rewrite API, set API_ENDPOINT to the POST URL.
// Until then, MODE stays "mock" and the rewrite step returns a deterministic
// stand-in so the UI is usable.
//
// API contract (when you build the backend):
//   POST <API_ENDPOINT>
//   Request body (JSON):
//     {
//       "library": "notifications",
//       "pattern": <the full notifications.json object>,
//       "input": "<user's draft or brief>"
//     }
//   Response body (JSON):
//     {
//       "rewrite": "<final conformant string>",
//       "notes": ["<optional LLM-side observations>"]
//     }
//
// The client-side grader runs the mechanical checks (length, link presence,
// urgency lead). Server-side grading can return richer notes in `notes`.

window.HEMINGWAY_CONFIG = {
  MODE: "api",                                // "mock" | "api"
  API_ENDPOINT: "https://hemingway-api.verbivoyeurista.workers.dev",                            // e.g. "https://your-worker.example.workers.dev/rewrite"
  LIBRARY_ENTRIES: ["notifications"],          // patterns available in the selector
};
