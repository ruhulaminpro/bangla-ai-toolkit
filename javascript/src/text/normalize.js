/**
 * Bengali Unicode normalization.
 * @param {string} text
 * @param {{ stripZeroWidth?: boolean, normalizePunct?: boolean }} [opts]
 * @returns {string}
 */
export function normalize(text, { stripZeroWidth = true, normalizePunct = true } = {}) {
  // NFC composition (ড + ় → ড়)
  text = text.normalize("NFC");

  if (stripZeroWidth) {
    // Zero-width space, ZWNJ, ZWJ, BOM
    text = text.replace(/[​‌‍﻿]/g, "");
  }

  if (normalizePunct) {
    text = text
      .replace(/[""]/g, '"')
      .replace(/['']/g, "'")
      .replace(/[–—]/g, "-")
      .replace(/ /g, " ");
  }

  return text.replace(/ {2,}/g, " ").trim();
}
