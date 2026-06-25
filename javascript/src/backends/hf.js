/**
 * HuggingFace Inference API backend — free tier available.
 * Requires: npm install @huggingface/inference
 */

const STAR_TO_LABEL = {
  "1 star": "negative", "2 stars": "negative",
  "3 stars": "neutral",
  "4 stars": "positive", "5 stars": "positive",
};

export class HuggingFaceBackend {
  /**
   * @param {{
   *   apiKey?: string,
   *   summarizerModel?: string,
   *   qaModel?: string,
   *   sentimentModel?: string,
   * }} opts
   */
  constructor({
    apiKey,
    summarizerModel = "csebuetnlp/mT5_multilingual_XLSum",
    qaModel = "deepset/xlm-roberta-base-squad2",
    sentimentModel = "nlptown/bert-base-multilingual-uncased-sentiment",
    nerModel = "Davlan/xlm-roberta-base-ner-hrl",
    embeddingModel = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  } = {}) {
    this._apiKey = apiKey ?? process.env.HF_TOKEN;
    this._summarizerModel = summarizerModel;
    this._qaModel = qaModel;
    this._sentimentModel = sentimentModel;
    this._nerModel = nerModel;
    this._embeddingModel = embeddingModel;
  }

  async _client() {
    const { HfInference } = await import("@huggingface/inference");
    if (!this._hf) this._hf = new HfInference(this._apiKey);
    return this._hf;
  }

  async summarize(text, { language = "bengali" } = {}) {
    const hf = await this._client();
    const prefix = language === "bengali" ? "bengali: " : "english: ";
    const result = await hf.summarization({
      model: this._summarizerModel,
      inputs: prefix + text,
      parameters: { max_new_tokens: 200, min_new_tokens: 20 },
    });
    return result.summary_text.trim();
  }

  async qa(context, question) {
    const hf = await this._client();
    const result = await hf.questionAnswering({
      model: this._qaModel,
      inputs: { question, context },
    });
    return result.answer.trim();
  }

  async sentiment(text) {
    const hf = await this._client();
    const results = await hf.textClassification({
      model: this._sentimentModel,
      inputs: text,
    });
    const top = results[0];
    const label = STAR_TO_LABEL[top.label.toLowerCase()] ?? top.label.toLowerCase();
    return { label, score: Math.round(top.score * 10000) / 10000, explanation: "" };
  }

  async ner(text) {
    const hf = await this._client();
    const results = await hf.tokenClassification({
      model: this._nerModel,
      inputs: text,
    });
    return results.map((r) => ({
      text: r.word,
      type: r.entity_group ?? r.entity,
      score: Math.round(r.score * 10000) / 10000,
    }));
  }

  async embed(texts) {
    const inputs = Array.isArray(texts) ? texts : [texts];
    const hf = await this._client();
    const vectors = [];
    for (const t of inputs) {
      const out = await hf.featureExtraction({ model: this._embeddingModel, inputs: t });
      // featureExtraction may return [hidden] (sentence model) or [tokens][hidden]
      vectors.push(Array.isArray(out[0]) ? meanPool(out) : out);
    }
    return vectors;
  }
}

function meanPool(tokenVecs) {
  const dim = tokenVecs[0].length;
  const pooled = new Array(dim).fill(0);
  for (const tok of tokenVecs) {
    for (let d = 0; d < dim; d++) pooled[d] += tok[d];
  }
  return pooled.map((x) => x / tokenVecs.length);
}
