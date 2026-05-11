import { BanglaAI } from "../src/index.js";

const ai = new BanglaAI({ apiKey: process.env.OPENAI_API_KEY });

const text =
  "বাংলাদেশ দক্ষিণ এশিয়ার একটি দেশ। এর রাজধানী ঢাকা। " +
  "বাংলাদেশের মোট জনসংখ্যা প্রায় ১৭ কোটি। " +
  "দেশটি ১৯৭১ সালে স্বাধীনতা লাভ করে।";

// Summarization
console.log("=== Summarization ===");
console.log(await ai.summarize.call(text, { maxSentences: 2 }));
console.log();

// Question Answering
const context =
  "রবীন্দ্রনাথ ঠাকুর ১৮৬১ সালে কলকাতায় জন্মগ্রহণ করেন। " +
  "তিনি ১৯১৩ সালে সাহিত্যে নোবেল পুরস্কার লাভ করেন।";

console.log("=== Question Answering ===");
console.log(await ai.qa.call(context, "রবীন্দ্রনাথ কোথায় জন্মগ্রহণ করেন?"));
console.log();

// Sentiment Analysis
console.log("=== Sentiment Analysis ===");
const result = await ai.sentiment.call(
  "আজকের দিনটি অসাধারণ ছিল! সব কিছু ভালো হয়েছে।"
);
console.log(`Label: ${result.label}`);
console.log(`Score: ${result.score.toFixed(2)}`);
console.log(`Explanation: ${result.explanation}`);
