import { describe, test, expect } from "@jest/globals";
import { text } from "../src/index.js";

describe("numerals", () => {
  test("bengali -> english digits", () => {
    expect(text.toEnglishDigits("২০২৪")).toBe("2024");
    expect(text.toEnglishDigits("৫টি আপেল")).toBe("5টি আপেল");
  });
  test("english -> bengali digits", () => {
    expect(text.toBengaliDigits("2024")).toBe("২০২৪");
    expect(text.toBengaliDigits("page 7")).toBe("page ৭");
  });
  test("roundtrip", () => {
    const s = "১২৩৪৫৬৭৮৯০";
    expect(text.toBengaliDigits(text.toEnglishDigits(s))).toBe(s);
  });
  test("non-digits untouched", () => {
    expect(text.toEnglishDigits("বাংলা")).toBe("বাংলা");
  });
});

describe("toLatin", () => {
  test("common words", () => {
    expect(text.toLatin("বাংলা")).toBe("bangla");
    expect(text.toLatin("ঢাকা")).toBe("dhaka");
    expect(text.toLatin("আমি")).toBe("ami");
    expect(text.toLatin("কলম")).toBe("kolom");
  });
  test("drops final schwa", () => {
    expect(text.toLatin("বাংলাদেশ")).toBe("bangladesh");
    expect(text.toLatin("মন")).toBe("mon");
  });
  test("keeps matra", () => {
    expect(text.toLatin("ভালো")).toBe("bhalo");
  });
  test("passthrough", () => {
    expect(text.toLatin("ঢাকা 2024")).toBe("dhaka 2024");
  });
});

describe("toBengali", () => {
  test("common words", () => {
    expect(text.toBengali("bangla")).toBe("বাংলা");
    expect(text.toBengali("ami")).toBe("আমি");
    expect(text.toBengali("kolom")).toBe("কলম");
    expect(text.toBengali("amar")).toBe("আমার");
  });
  test("conjunct uses hasanta", () => {
    expect(text.toBengali("dhonnobad")).toContain("্");
  });
  test("passthrough", () => {
    expect(text.toBengali("bangla 2024")).toBe("বাংলা 2024");
  });
});
