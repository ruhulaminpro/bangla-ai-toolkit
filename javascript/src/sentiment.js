const SYSTEM = `You are a Bengali sentiment analysis expert.
Analyze the sentiment of Bengali text and return a JSON object with:
  - "label": one of "positive", "negative", or "neutral"
  - "score": confidence float between 0.0 and 1.0
  - "explanation": one-sentence reason in Bengali

Return only valid JSON. No markdown, no extra text.`;

export class Sentiment {
  constructor(client, model = "gpt-4o-mini") {
    this._client = client;
    this._model = model;
  }

  /**
   * Classify sentiment of Bengali text.
   * @param {string} text  Bengali input text
   * @returns {Promise<{label: string, score: number, explanation: string}>}
   */
  async call(text) {
    const response = await this._client.chat.completions.create({
      model: this._model,
      messages: [
        { role: "system", content: SYSTEM },
        { role: "user", content: text },
      ],
      temperature: 0.0,
      response_format: { type: "json_object" },
    });

    return JSON.parse(response.choices[0].message.content);
  }
}
