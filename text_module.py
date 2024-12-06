from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)
import pymorphy2
import re

def get_text_in_normal_form(text):
    morph = pymorphy2.MorphAnalyzer(lang="ru")
    segmenter = Segmenter()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)

    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    massive = []
    for sent in doc.sents:
        syntax = sent.syntax
        for token in syntax.tokens:
            p = morph.parse(token.text)[0]
            massive += [p.normal_form.strip()]
    return " ".join(massive)

#text = open('constitution.txt', encoding="utf8").read()


def find_childs(head_id, tokens):
    result = ""
    white_list = ["amod", "nmod", "nsubj", "conj", "obj", "obl", "root"]
    for token in tokens:
        if ((token.head_id == head_id) or (token.id == head_id)) and (token.rel in white_list):
            result += f"{token.text} "
    return result.strip()
        

def get_slovosochetaniya(text):
    morph = pymorphy2.MorphAnalyzer(lang="ru")
    segmenter = Segmenter()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)

    doc = Doc(text)
    heads = []
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    massive = []
    for sent in doc.sents:
        syntax = sent.syntax
        for token in syntax.tokens:
            if ((token.rel) == "amod" and (token.head_id not in heads)):
                heads += [token.head_id.strip()]
                massive += [find_childs(token.head_id, syntax.tokens).strip()]
    return massive