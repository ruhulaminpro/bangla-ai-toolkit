import { OpenAIBackend } from "./backends/openai.js";
import { HuggingFaceBackend } from "./backends/hf.js";
import { rankBySimilarity } from "./semantic.js";

export class BanglaAI {
  /**
   * @param {{
   *   backend?: "openai" | "huggingface" | object,
   *   apiKey?: string,
   *   model?: string,
   * }} [opts]
   */
  constructor({ backend = "huggingface", apiKey, model } = {}) {
    if (typeof backend === "object") {
      this._backend = backend;
    } else if (backend === "openai") {
      this._backend = new OpenAIBackend({ apiKey, model });
    } else if (backend === "huggingface") {
      this._backend = new HuggingFaceBackend({ apiKey });
    } else {
      throw new Error(`Unknown backend: "${backend}". Use "openai" or "huggingface".`);
    }
  }

  summarize(text, opts) { return this._backend.summarize(text, opts); }
  qa(context, question, opts) { return this._backend.qa(context, question, opts); }
  sentiment(text) { return this._backend.sentiment(text); }

  /** Extract named entities. Returns [{ text, type, score }]. */
  ner(text) { return this._backend.ner(text); }

  /** Embed a string or array of strings into vectors. */
  embed(texts) {
    return this._backend.embed(Array.isArray(texts) ? texts : [texts]);
  }

  /**
   * Rank documents by semantic similarity to a query.
   * @param {string} query
   * @param {string[]} documents
   * @param {{ topK?: number }} [opts]
   * @returns {Promise<{document: string, score: number, index: number}[]>}
   */
  async semanticSearch(query, documents, { topK = 5 } = {}) {
    const vectors = await this._backend.embed([query, ...documents]);
    const [queryVec, ...docVecs] = vectors;
    return rankBySimilarity(queryVec, docVecs)
      .slice(0, topK)
      .map(({ index, score }) => ({
        document: documents[index],
        score: Math.round(score * 10000) / 10000,
        index,
      }));
  }
}
