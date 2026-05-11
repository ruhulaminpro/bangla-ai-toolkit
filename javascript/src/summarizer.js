const SYSTEM = `You are an expert Bengali language summarizer.
Summarize the provided Bengali text clearly and concisely.
Preserve key information and maintain the original language (Bengali).
Output only the summary — no preamble, no explanations.`;

export class Summarizer {
  constructor(client, model = "gpt-4o-mini") {
    this._client = client;
    this._model = model;
  }

  /**
   * Summarize Bengali text.
   * @param {string} text  Bengali input text
   * @param {object} [options]
   * @param {number} [options.maxSentences=3]  Target summary length
   * @param {string} [options.language="bengali"]  Output language: "bengali" | "english"
   * @returns {Promise<string>}
   */
  async call(text, { maxSentences = 3, language = "bengali" } = {}) {
    const langInstruction =
      language === "bengali"
        ? "Respond in Bengali (বাংলা)."
        : "Respond in English.";

    const userPrompt =
      `Summarize the following text in ${maxSentences} sentences or fewer. ` +
      `${langInstruction}\n\nText:\n${text}`;

    const response = await this._client.chat.completions.create({
      model: this._model,
      messages: [
        { role: "system", content: SYSTEM },
        { role: "user", content: userPrompt },
      ],
      temperature: 0.3,
    });

    return response.choices[0].message.content.trim();
  }
}
