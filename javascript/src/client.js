import { OpenAIBackend } from "./backends/openai.js";
import { HuggingFaceBackend } from "./backends/hf.js";

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
}
