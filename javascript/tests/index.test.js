import { describe, test, expect } from "@jest/globals";
import { text } from "../src/index.js";

describe("text.normalize", () => {
  test("collapses multiple spaces", () => {
    expect(text.normalize("বাংলা  টেক্সট")).toBe("বাংলা টেক্সট");
  });
  test("strips zero-width characters", () => {
    expect(text.normalize("বাংলা​টেক্সট")).not.toContain("​");
  });
});

describe("text.tokenize", () => {
  test("returns word tokens, drops punctuation", () => {
    const tokens = text.tokenize("আমি বাংলায় কথা বলি।");
    expect(tokens).toContain("আমি");
    expect(tokens).toContain("বাংলায়");
    expect(tokens).not.toContain("।");
  });
  test("handles mixed script", () => {
    const tokens = text.tokenize("LXNotes ২০২৪ সালে শুরু হয়।");
    expect(tokens).toContain("LXNotes");
    expect(tokens).toContain("২০২৪");
  });
});

describe("text.sentTokenize", () => {
  test("splits on daṇḍa", () => {
    const sents = text.sentTokenize("আমি বাংলায় কথা বলি। তুমি কেমন আছ?");
    expect(sents.length).toBe(2);
  });
});

describe("text.removeStopwords", () => {
  test("removes known stopwords", () => {
    const tokens = text.tokenize("আমি বাংলাদেশে যাই।");
    const filtered = text.removeStopwords(tokens);
    expect(filtered).not.toContain("আমি");
    expect(filtered).toContain("বাংলাদেশে");
  });
});

describe("text.stem", () => {
  test("strips verbal suffix", () => {
    expect(text.stem("করেছেন")).toBe("কর");
  });
  test("strips nominal suffix", () => {
    expect(text.stem("বাংলাদেশের")).toBe("বাংলাদেশ");
  });
  test("no change for short words", () => {
    expect(text.stem("বই")).toBe("বই");
  });
});
