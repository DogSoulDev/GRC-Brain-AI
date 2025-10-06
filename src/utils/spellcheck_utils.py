"""
spellcheck_utils.py - English-only spellchecking utility for DsD GRC AI
"""
from spellchecker import SpellChecker

class SpellcheckUtils:
    def spacy_phrase_match(self, text, patterns=None):
        """
        Use spaCy PhraseMatcher to detect regulatory, legal, compliance, and colloquial phrases in text.
        patterns: list of phrases to match (official terms, colloquial phrases, etc.)
        Returns list of matched phrases.
        """
        import spacy
        from spacy.matcher import PhraseMatcher
        nlp = spacy.load("en_core_web_sm")
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        if patterns is None:
            # Official regulatory/legal terms and common colloquial phrases
            patterns = [
                "nist", "gdpr", "hipaa", "sox", "fisma", "cisa", "enisa", "iso 27001", "cybersecurity framework",
                "risk management", "compliance", "data protection", "privacy", "incident response", "threat intelligence",
                "what's up", "how are you", "good morning", "good afternoon", "good evening", "yo", "sup"
            ]
        phrase_patterns = [nlp.make_doc(p) for p in patterns]
        matcher.add("GRC_PHRASES", phrase_patterns)
        doc = nlp(text)
        matches = matcher(doc)
        return [doc[start:end].text for _, start, end in matches]
    def preprocess_input(self, text):
        """
        Preprocess user input: spellcheck, autocorrect, and phrase match for regulatory/legal/colloquial terms.
        Returns dict with corrected text, misspelled words, suggestions, and matched phrases.
        """
        spell_result = self.check_spelling(text)
        corrected = self.autocorrect(text)
        matched_phrases = self.spacy_phrase_match(corrected)
        return {
            'original': text,
            'corrected': corrected,
            'misspelled': spell_result['misspelled'],
            'suggestions': spell_result['suggestions'],
            'matched_phrases': matched_phrases
        }
    def __init__(self):
        from spellchecker import SpellChecker
        self.spell_en = SpellChecker(language='en')  # US English

    def check_spelling(self, text):
        spell = self.spell_en
        words = text.split()
        misspelled = list(spell.unknown(words))
        suggestions = {}
        for word in misspelled:
            candidates = spell.candidates(word)
            if candidates:
                suggestions[word] = list(candidates)
            else:
                suggestions[word] = []
        return {'misspelled': misspelled, 'suggestions': suggestions}

    def autocorrect(self, text):
        spell = self.spell_en
        words = text.split()
        corrected = []
        for word in words:
            if word in spell:
                corrected.append(word)
            else:
                candidates = spell.candidates(word)
                if candidates and isinstance(candidates, set):
                    best = next(iter(candidates))
                else:
                    best = word
                corrected.append(best)
        return ' '.join(corrected)
