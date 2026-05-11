const WORD_RE = /[ঀ-৿]+|[0-9০-৯]+|[a-zA-Z]+/g;
const SENT_RE = /[।॥!?]+|\.{1,3}/;

/**
 * Tokenize Bengali text into words.
 * @param {string} text
 * @returns {string[]}
 */
export function tokenize(text) {
  return text.match(WORD_RE) ?? [];
}

/**
 * Split text into sentences.
 * @param {string} text
 * @returns {string[]}
 */
export function sentTokenize(text) {
  return text.split(SENT_RE).map((s) => s.trim()).filter(Boolean);
}
