import { describe, test, expect } from "@jest/globals";
import { BanglaAI, cosineSimilarity, rankBySimilarity } from "../src/index.js";

// Fake backend: returns canned vectors/entities, no API needed.
class FakeBackend {
  constructor(vectors) { this._vectors = vectors; }
  async embed(texts) { return texts.map((t) => this._vectors[t]); }
  async ner() { return [{ text: "ঢাকা", type: "LOC", score: 0.99 }]; }
}

describe("cosineSimilarity", () => {
  test("identical vectors -> 1", () => {
    expect(cosineSimilarity([1, 2, 3], [1, 2, 3])).toBeCloseTo(1.0);
  });
  test("orthogonal -> 0", () => {
    expect(cosineSimilarity([1, 0], [0, 1])).toBeCloseTo(0.0);
  });
  test("zero vector -> 0", () => {
    expect(cosineSimilarity([0, 0], [1, 1])).toBe(0);
  });
});

describe("rankBySimilarity", () => {
  test("orders by similarity", () => {
    const ranked = rankBySimilarity([1, 0], [[0, 1], [1, 0.1], [-1, 0]]);
    expect(ranked[0].index).toBe(1);
    expect(ranked[ranked.length - 1].index).toBe(2);
  });
});

describe("BanglaAI semantic + ner wiring", () => {
  test("semanticSearch ranks documents", async () => {
    const vectors = {
      "রাজধানী": [1, 0],
      "ঢাকা বাংলাদেশের রাজধানী": [1, 0.1],
      "আমি ভাত খাই": [0, 1],
    };
    const ai = new BanglaAI({ backend: new FakeBackend(vectors) });
    const results = await ai.semanticSearch("রাজধানী", ["ঢাকা বাংলাদেশের রাজধানী", "আমি ভাত খাই"], { topK: 2 });
    expect(results[0].document).toBe("ঢাকা বাংলাদেশের রাজধানী");
    expect(results[0].index).toBe(0);
    expect(results[0].score).toBeGreaterThanOrEqual(results[1].score);
  });

  test("ner passes through backend", async () => {
    const ai = new BanglaAI({ backend: new FakeBackend({}) });
    const entities = await ai.ner("ঢাকা একটি শহর");
    expect(entities[0].type).toBe("LOC");
  });
});
