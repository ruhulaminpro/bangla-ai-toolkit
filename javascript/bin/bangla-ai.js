#!/usr/bin/env node
/**
 * Command-line interface for bangla-ai.
 *
 * Text-utility commands run with zero dependencies. ML commands (summarize,
 * qa, sentiment, ner) require a backend and its peer dependency.
 *
 *   bangla-ai normalize "বাংলা   টেক্সট"
 *   bangla-ai translit --to latin "বাংলাদেশ"
 *   bangla-ai digits --to bn "2024"
 *   echo "..." | bangla-ai tokenize -
 *   bangla-ai sentiment "..." --backend openai
 */

import { text, BanglaAI } from "../src/index.js";

function parseFlags(args) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      flags[args[i].slice(2)] = args[i + 1];
      i++;
    } else {
      positional.push(args[i]);
    }
  }
  return { flags, positional };
}

async function readInput(value) {
  if (value !== "-") return value;
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8").trim();
}

function out(value) {
  console.log(typeof value === "string" ? value : JSON.stringify(value, null, 2));
}

function makeAI(flags) {
  return new BanglaAI({
    backend: flags.backend ?? "huggingface",
    apiKey: flags["api-key"],
    model: flags.model,
  });
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  const { flags, positional } = parseFlags(rest);

  if (!command || command === "--help" || command === "-h") {
    console.log("Usage: bangla-ai <normalize|tokenize|stem|translit|digits|summarize|qa|sentiment|ner> <text> [flags]");
    return;
  }

  const body = await readInput(positional[0] ?? "-");

  switch (command) {
    case "normalize": return out(text.normalize(body));
    case "tokenize": return out(text.tokenize(body));
    case "stem": return out(text.stemTokens(text.tokenize(body)));
    case "translit":
      return out(flags.to === "latin" ? text.toLatin(body) : text.toBengali(body));
    case "digits":
      return out(flags.to === "en" ? text.toEnglishDigits(body) : text.toBengaliDigits(body));
    case "summarize":
      return out(await makeAI(flags).summarize(body, { maxSentences: Number(flags["max-sentences"] ?? 3) }));
    case "qa":
      return out(await makeAI(flags).qa(body, flags.question));
    case "sentiment":
      return out(await makeAI(flags).sentiment(body));
    case "ner":
      return out(await makeAI(flags).ner(body));
    default:
      console.error(`Unknown command: ${command}`);
      process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exitCode = 1;
});
