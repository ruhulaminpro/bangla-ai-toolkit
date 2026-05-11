import { describe, test, expect, beforeAll } from "@jest/globals";
import { BanglaAI } from "../src/index.js";

const CONTEXT =
  "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। " +
  "তিনি ১৯১৩ সালে সাহিত্যে নোবেল পুরস্কার লাভ করেন।";

let ai;

beforeAll(() => {
  if (!process.env.OPENAI_API_KEY) {
    console.warn("OPENAI_API_KEY not set — skipping live tests");
  }
  ai = new BanglaAI({ apiKey: process.env.OPENAI_API_KEY });
});

describe("Summarizer", () => {
  test("returns non-empty string", async () => {
    if (!process.env.OPENAI_API_KEY) return;
    const result = await ai.summarize.call(CONTEXT, { maxSentences: 1 });
    expect(typeof result).toBe("string");
    expect(result.length).toBeGreaterThan(0);
  });
});

describe("QA", () => {
  test("answers question from context", async () => {
    if (!process.env.OPENAI_API_KEY) return;
    const answer = await ai.qa.call(
      CONTEXT,
      "When was Tagore born?",
      { language: "english" }
    );
    expect(answer).toContain("1861");
  });
});

describe("Sentiment", () => {
  test("classifies positive text", async () => {
    if (!process.env.OPENAI_API_KEY) return;
    const result = await ai.sentiment.call(
      "আজকের দিনটি অসাধারণ ছিল! আমি খুব খুশি।"
    );
    expect(result.label).toBe("positive");
    expect(typeof result.score).toBe("number");
    expect(result.score).toBeGreaterThanOrEqual(0);
    expect(result.score).toBeLessThanOrEqual(1);
  });
});
