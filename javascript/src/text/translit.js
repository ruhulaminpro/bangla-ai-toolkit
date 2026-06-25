/**
 * Bengali transliteration (romanization and phonetic input).
 *
 *  - toLatin   — Bengali script → Latin (romanization). Deterministic.
 *  - toBengali — Latin "Banglish" → Bengali script (phonetic typing).
 *
 * Both are APPROXIMATE. Bengali↔Latin has no lossless mapping: romanization
 * drops vowel-length distinctions and phonetic input is ambiguous (e.g. "t"
 * could be ত or ট). These aim to be correct on common chat/search words, not
 * to be a reversible codec. See the test suite for guaranteed cases.
 */

// ── Bengali → Latin ───────────────────────────────────────────────────────────

const INDEP_VOWELS = {
  অ: "o", আ: "a", ই: "i", ঈ: "i", উ: "u", ঊ: "u",
  ঋ: "ri", এ: "e", ঐ: "oi", ও: "o", ঔ: "ou",
};

const MATRAS = {
  "া": "a", "ি": "i", "ী": "i", "ু": "u", "ূ": "u", "ৃ": "ri",
  "ে": "e", "ৈ": "oi", "ো": "o", "ৌ": "ou",
};

const CONSONANTS = {
  ক: "k", খ: "kh", গ: "g", ঘ: "gh", ঙ: "ng",
  চ: "ch", ছ: "chh", জ: "j", ঝ: "jh", ঞ: "n",
  ট: "t", ঠ: "th", ড: "d", ঢ: "dh", ণ: "n",
  ত: "t", থ: "th", দ: "d", ধ: "dh", ন: "n",
  প: "p", ফ: "ph", ব: "b", ভ: "bh", ম: "m",
  য: "j", র: "r", ল: "l", শ: "sh", ষ: "sh",
  স: "s", হ: "h", "ড়": "r", "ঢ়": "rh", "য়": "y", "ৎ": "t",
};

const SIGNS = { "ং": "ng", "ঃ": "h", "ঁ": "n" };

const HASANTA = "্";
const INHERENT = "o";

/**
 * Romanize Bengali script to Latin (approximate).
 * @param {string} text
 * @returns {string}
 */
export function toLatin(text) {
  const out = [];
  let i = 0;
  const n = text.length;
  while (i < n) {
    const ch = text[i];
    if (ch in CONSONANTS) {
      out.push(CONSONANTS[ch]);
      const nxt = i + 1 < n ? text[i + 1] : "";
      if (nxt === HASANTA) { i += 2; continue; }        // conjunct
      if (nxt in MATRAS) { out.push(MATRAS[nxt]); i += 2; continue; }
      // Inherent vowel, dropped word-finally (schwa deletion).
      if (nxt in CONSONANTS || nxt in INDEP_VOWELS || nxt in SIGNS) {
        out.push(INHERENT);
      }
      i += 1;
      continue;
    }
    if (ch in INDEP_VOWELS) out.push(INDEP_VOWELS[ch]);
    else if (ch in SIGNS) out.push(SIGNS[ch]);
    else if (ch in MATRAS) out.push(MATRAS[ch]);
    else out.push(ch);
    i += 1;
  }
  return out.join("");
}

// ── Latin → Bengali ───────────────────────────────────────────────────────────

const LATIN_INDEP = {
  ou: "ঔ", oi: "ঐ", oo: "ঊ", ee: "ঈ", aa: "আ",
  a: "আ", i: "ই", u: "উ", e: "এ", o: "অ", O: "ও",
};

const LATIN_MATRA = {
  ou: "ৌ", oi: "ৈ", oo: "ূ", ee: "ী", aa: "া",
  a: "া", i: "ি", u: "ু", e: "ে", O: "ো",
};

const LATIN_CONSONANTS = {
  chh: "ছ", kh: "খ", gh: "ঘ", ng: "ং", ch: "চ",
  jh: "ঝ", th: "থ", dh: "ধ", ph: "ফ", bh: "ভ",
  sh: "শ", rh: "ঢ়",
  k: "ক", g: "গ", j: "জ", t: "ত", d: "দ", n: "ন",
  p: "প", b: "ব", m: "ম", r: "র", l: "ল", s: "স",
  h: "হ", y: "য়", w: "ও", v: "ভ", f: "ফ", z: "জ",
};

const byLenDesc = (a, b) => b.length - a.length;
const VOWEL_KEYS = [...new Set([...Object.keys(LATIN_INDEP), ...Object.keys(LATIN_MATRA), "o"])].sort(byLenDesc);
const CONS_KEYS = Object.keys(LATIN_CONSONANTS).sort(byLenDesc);

/**
 * Convert Latin "Banglish" to Bengali script (approximate, phonetic).
 * @param {string} text
 * @returns {string}
 */
export function toBengali(text) {
  const out = [];
  let prevConsonant = false;
  let i = 0;
  const n = text.length;
  while (i < n) {
    let matched = CONS_KEYS.find((k) => text.startsWith(k, i));
    if (matched !== undefined) {
      if (prevConsonant) out.push(HASANTA);
      out.push(LATIN_CONSONANTS[matched]);
      prevConsonant = matched !== "ng";   // "ng" is anusvara, not a base
      i += matched.length;
      continue;
    }
    matched = VOWEL_KEYS.find((k) => text.startsWith(k, i));
    if (matched !== undefined) {
      if (prevConsonant) {
        if (matched !== "o") out.push(LATIN_MATRA[matched] ?? "");
      } else {
        out.push(LATIN_INDEP[matched] ?? "");
      }
      prevConsonant = false;
      i += matched.length;
      continue;
    }
    out.push(text[i]);
    prevConsonant = false;
    i += 1;
  }
  return out.join("");
}
