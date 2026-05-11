// Ordered longest → shortest — more specific suffix must precede shorter ones
const SUFFIXES = [
  // Perfect (must precede present-continuous ছেন)
  ["েছিলেন",2],["েছিলাম",2],["েছিলে",2],["েছিলো",2],
  ["েছেন",2],["েছে",2],["েছি",2],["েছো",2],
  // Past imperfect
  ["চ্ছিলেন",2],["চ্ছিলাম",2],["চ্ছিলে",2],["চ্ছিলো",2],["চ্ছিল",2],
  ["ছিলেন",2],["ছিলাম",2],["ছিলে",2],["ছিলো",2],["ছিল",2],
  // Present continuous
  ["চ্ছেন",2],["চ্ছে",2],["চ্ছি",2],["চ্ছো",2],
  ["ছেন",2],["ছে",2],["ছি",2],["ছো",2],
  // Simple past
  ["লেন",2],["লাম",2],["লো",2],["লে",2],["ল",2],
  // Future
  ["বেন",2],["বো",2],["বে",2],["বি",2],
  // Imperative / present
  ["উন",2],["ুন",2],["েন",2],
  // Plural
  ["গুলোকে",2],["গুলোর",2],["গুলো",2],
  ["েরকে",2],["েরও",2],["েরা",2],
  ["দেরকে",2],["দেরও",2],["দের",2],
  ["রাকে",2],["রারও",2],["রা",2],
  // Case markers
  ["ের",2],["তেও",2],["তে",2],["কেও",2],["কে",2],["র",2],
  // Derivational
  ["আনো",2],["ওয়া",2],["িত",2],
];

/**
 * Strip inflectional suffixes from a Bengali word.
 * @param {string} word
 * @returns {string}
 */
export function stem(word) {
  for (const [suffix, minLen] of SUFFIXES) {
    if (word.endsWith(suffix) && word.length - suffix.length >= minLen) {
      return word.slice(0, -suffix.length);
    }
  }
  return word;
}

/**
 * Stem an array of tokens.
 * @param {string[]} tokens
 * @returns {string[]}
 */
export function stemTokens(tokens) {
  return tokens.map(stem);
}
