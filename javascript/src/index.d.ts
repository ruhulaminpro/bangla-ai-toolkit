// Type definitions for bangla-ai

export interface Entity {
  text: string;
  type: string;
  score: number;
}

export interface SentimentResult {
  label: string;
  score: number;
  explanation: string;
}

export interface SearchResult {
  document: string;
  score: number;
  index: number;
}

export interface Backend {
  summarize(text: string, opts?: { maxSentences?: number; language?: string }): Promise<string>;
  qa(context: string, question: string, opts?: { language?: string }): Promise<string>;
  sentiment(text: string): Promise<SentimentResult>;
  ner?(text: string): Promise<Entity[]>;
  embed?(texts: string[]): Promise<number[][]>;
}

export interface BanglaAIOptions {
  backend?: "openai" | "huggingface" | Backend;
  apiKey?: string;
  model?: string;
}

export class BanglaAI {
  constructor(opts?: BanglaAIOptions);
  summarize(text: string, opts?: { maxSentences?: number; language?: string }): Promise<string>;
  qa(context: string, question: string, opts?: { language?: string }): Promise<string>;
  sentiment(text: string): Promise<SentimentResult>;
  ner(text: string): Promise<Entity[]>;
  embed(texts: string | string[]): Promise<number[][]>;
  semanticSearch(query: string, documents: string[], opts?: { topK?: number }): Promise<SearchResult[]>;
}

export function cosineSimilarity(a: number[], b: number[]): number;
export function rankBySimilarity(
  queryVec: number[],
  docVecs: number[][]
): { index: number; score: number }[];

export namespace text {
  function normalize(text: string, opts?: { stripZeroWidth?: boolean; normalizePunct?: boolean }): string;
  function tokenize(text: string): string[];
  function sentTokenize(text: string): string[];
  const STOPWORDS: Set<string>;
  function removeStopwords(tokens: string[]): string[];
  function stem(word: string): string;
  function stemTokens(tokens: string[]): string[];
  function toEnglishDigits(text: string): string;
  function toBengaliDigits(text: string): string;
  function toLatin(text: string): string;
  function toBengali(text: string): string;
}
