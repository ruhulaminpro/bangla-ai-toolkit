import { BanglaAI, text } from "../src/index.js";

// ── Text utilities (zero deps) ─────────────────────────────────────────────────
const raw = "বাংলাদেশ   দক্ষিণ এশিয়ার একটি দেশ।  এর রাজধানী ঢাকা।";

console.log("=== Text Utilities ===");
const normalized = text.normalize(raw);
const tokens = text.tokenize(normalized);
console.log("normalized :", normalized);
console.log("tokens     :", tokens);
console.log("sentences  :", text.sentTokenize(normalized));
console.log("filtered   :", text.removeStopwords(tokens));
console.log("stems      :", text.stemTokens(text.removeStopwords(tokens)));
console.log();

// ── HuggingFace backend (free, set HF_TOKEN env var) ──────────────────────────
// const ai = new BanglaAI();  // backend: "huggingface"

// ── OpenAI backend ────────────────────────────────────────────────────────────
const ai = new BanglaAI({ backend: "openai", apiKey: process.env.OPENAI_API_KEY });

const passage =
  "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।";

console.log("=== Summarization ===");
console.log(await ai.summarize(passage, { maxSentences: 1 }));

console.log("\n=== Question Answering ===");
console.log(await ai.qa(passage, "বাংলাদেশের রাজধানী কোথায়?"));

console.log("\n=== Sentiment ===");
const r = await ai.sentiment("আজকের দিনটি অসাধারণ ছিল!");
console.log(`label: ${r.label}  score: ${r.score.toFixed(2)}`);
