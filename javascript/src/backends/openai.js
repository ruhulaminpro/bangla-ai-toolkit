const SUM_SYSTEM =
  "You are an expert Bengali language summarizer. Output only the summary — no preamble.";
const QA_SYSTEM =
  "You are a Bengali question answering assistant. Answer strictly from the provided context.";
const SENT_SYSTEM =
  'Bengali sentiment analysis expert. Return JSON: {"label":"positive|negative|neutral","score":0.0-1.0,"explanation":"one sentence in Bengali"}. Only JSON.';
const NER_SYSTEM =
  'You are a Bengali named-entity recognition system. Extract entities and return JSON {"entities":[{"text":"...","type":"PER|LOC|ORG|MISC"}]}. Use the exact surface form from the text. Only JSON.';

export class OpenAIBackend {
  /** @param {{ apiKey?: string, model?: string, embeddingModel?: string }} opts */
  constructor({ apiKey, model = "gpt-4o-mini", embeddingModel = "text-embedding-3-small" } = {}) {
    this._apiKey = apiKey ?? process.env.OPENAI_API_KEY;
    this._model = model;
    this._embeddingModel = embeddingModel;
  }

  async _openai() {
    const { default: OpenAI } = await import("openai");
    if (!this._client) this._client = new OpenAI({ apiKey: this._apiKey });
    return this._client;
  }

  async _chat(system, user, { temperature = 0.3, jsonMode = false } = {}) {
    const client = await this._openai();
    const params = {
      model: this._model,
      messages: [{ role: "system", content: system }, { role: "user", content: user }],
      temperature,
    };
    if (jsonMode) params.response_format = { type: "json_object" };

    const res = await client.chat.completions.create(params);
    return res.choices[0].message.content.trim();
  }

  async summarize(text, { maxSentences = 3, language = "bengali" } = {}) {
    const lang = language === "bengali" ? "Bengali (বাংলা)" : "English";
    return this._chat(SUM_SYSTEM, `Summarize in ${maxSentences} sentences. Respond in ${lang}.\n\n${text}`, { temperature: 0.3 });
  }

  async qa(context, question, { language = "bengali" } = {}) {
    const lang = language === "bengali" ? "Bengali (বাংলা)" : "English";
    return this._chat(QA_SYSTEM, `Context:\n${context}\n\nQuestion: ${question}\n\nAnswer in ${lang}.`, { temperature: 0.1 });
  }

  async sentiment(text) {
    const raw = await this._chat(SENT_SYSTEM, text, { temperature: 0.0, jsonMode: true });
    return JSON.parse(raw);
  }

  async ner(text) {
    const raw = await this._chat(NER_SYSTEM, text, { temperature: 0.0, jsonMode: true });
    return JSON.parse(raw).entities ?? [];
  }

  async embed(texts) {
    const input = Array.isArray(texts) ? texts : [texts];
    const client = await this._openai();
    const res = await client.embeddings.create({ model: this._embeddingModel, input });
    return res.data.map((item) => item.embedding);
  }
}
