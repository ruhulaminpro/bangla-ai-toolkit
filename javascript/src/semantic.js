/**
 * Vector similarity helpers — pure JS, zero dependencies.
 *
 * Used by BanglaAI.semanticSearch to rank documents against a query once a
 * backend has produced embeddings, but usable standalone with any vectors.
 */

/**
 * Cosine similarity of two equal-length vectors. Returns 0 if either vector
 * is all zeros.
 * @param {number[]} a
 * @param {number[]} b
 * @returns {number}
 */
export function cosineSimilarity(a, b) {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Rank documents by cosine similarity to the query.
 * @param {number[]} queryVec
 * @param {number[][]} docVecs
 * @returns {{index: number, score: number}[]} sorted by score, highest first
 */
export function rankBySimilarity(queryVec, docVecs) {
  return docVecs
    .map((d, index) => ({ index, score: cosineSimilarity(queryVec, d) }))
    .sort((a, b) => b.score - a.score);
}
