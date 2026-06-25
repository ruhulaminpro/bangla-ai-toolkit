/**
 * Bengali numeral conversion.
 *
 * Bengali uses its own digit glyphs (০-৯). These helpers convert between
 * Bengali and ASCII digits in both directions, leaving non-digits untouched.
 */

const BENGALI_DIGITS = "০১২৩৪৫৬৭৮৯";
const ASCII_DIGITS = "0123456789";

const BN_TO_EN = {};
const EN_TO_BN = {};
for (let d = 0; d < 10; d++) {
  BN_TO_EN[BENGALI_DIGITS[d]] = ASCII_DIGITS[d];
  EN_TO_BN[ASCII_DIGITS[d]] = BENGALI_DIGITS[d];
}

/**
 * Convert Bengali digits (০-৯) to ASCII digits (0-9).
 * @param {string} text
 * @returns {string}
 */
export function toEnglishDigits(text) {
  return text.replace(/[০-৯]/g, (c) => BN_TO_EN[c]);
}

/**
 * Convert ASCII digits (0-9) to Bengali digits (০-৯).
 * @param {string} text
 * @returns {string}
 */
export function toBengaliDigits(text) {
  return text.replace(/[0-9]/g, (c) => EN_TO_BN[c]);
}
