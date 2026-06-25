# Roadmap

Bengali (বাংলা) is the 6th-most-spoken language on Earth (230M+ speakers) yet has
a fraction of the open NLP infrastructure of comparably sized languages. The goal
of bangla-ai-toolkit is to be the default, batteries-included NLP layer for
Bengali across Python and JavaScript.

## Shipped (v0.2.0)
- Zero-dependency text utilities: normalize, tokenize, stopwords, stemmer
- Pluggable ML backends: HuggingFace (free) and OpenAI (paid)
- Summarization, question answering, sentiment — Python + JavaScript

## Near term
- **Bengali Named Entity Recognition (NER)** — person/place/org tagging
- Expanded stopword and stemmer rule coverage (dialectal + formal registers)
- Transliteration (Banglish ↔ Bengali) utilities
- Benchmark suite comparing backends on public Bengali datasets

## How OpenAI API credits accelerate this

Most Bengali NLP work is bottlenecked by the absence of high-quality labeled
data. We would use API credits to:

1. **Build open evaluation datasets** — use OpenAI models to generate and
   human-verify gold-standard Bengali summarization, QA, and NER examples,
   released publicly under a permissive license.
2. **Distill smaller models** — use a strong OpenAI model as a teacher to create
   compact, offline Bengali models shipped through the free HuggingFace backend,
   so the benefit reaches users without API budgets.
3. **Raise quality of the OpenAI backend** — tune prompts and few-shot examples
   per task, measured against the eval datasets above.

The result is a flywheel: credits fund open data and distilled models that make
the toolkit better for everyone, not just paying users.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs especially welcome for stopword/
stemmer rules, new model integrations, and NER.
