import OpenAI from "openai";
import { Summarizer } from "./summarizer.js";
import { QA } from "./qa.js";
import { Sentiment } from "./sentiment.js";

export class BanglaAI {
  /**
   * @param {object} [options]
   * @param {string} [options.apiKey]  OpenAI API key (falls back to OPENAI_API_KEY env)
   * @param {string} [options.model]   Model to use (default: "gpt-4o-mini")
   */
  constructor({ apiKey, model = "gpt-4o-mini" } = {}) {
    const client = new OpenAI({ apiKey });
    this.summarize = new Summarizer(client, model);
    this.qa = new QA(client, model);
    this.sentiment = new Sentiment(client, model);
  }
}
