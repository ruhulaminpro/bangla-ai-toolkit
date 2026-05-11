const SYSTEM = `You are an expert Bengali language question answering assistant.
Given a context passage in Bengali and a question, answer the question accurately.
Base your answer strictly on the provided context.
If the answer is not in the context, say so clearly in the same language as the question.`;

export class QA {
  constructor(client, model = "gpt-4o-mini") {
    this._client = client;
    this._model = model;
  }

  /**
   * Answer a question based on Bengali context.
   * @param {string} context  Bengali passage containing the answer
   * @param {string} question  Question in Bengali or English
   * @param {object} [options]
   * @param {string} [options.language="bengali"]  Response language: "bengali" | "english"
   * @returns {Promise<string>}
   */
  async call(context, question, { language = "bengali" } = {}) {
    const langInstruction =
      language === "bengali"
        ? "Answer in Bengali (বাংলা)."
        : "Answer in English.";

    const userPrompt =
      `Context:\n${context}\n\n` +
      `Question: ${question}\n\n` +
      langInstruction;

    const response = await this._client.chat.completions.create({
      model: this._model,
      messages: [
        { role: "system", content: SYSTEM },
        { role: "user", content: userPrompt },
      ],
      temperature: 0.1,
    });

    return response.choices[0].message.content.trim();
  }
}
