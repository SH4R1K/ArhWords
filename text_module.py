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

text = open('constitution.txt', encoding="utf8").read()


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

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    massive = []
    for sent in doc.sents:
        syntax = sent.syntax
        for token in syntax.tokens:
            if (token.rel == "amod"):
                massive += [find_childs(token.head_id, syntax.tokens).strip()]
    return massive
#print(get_slovosochetaniya(text))
# def find_phrases(text):
#     morph = pymorphy2.MorphAnalyzer(lang="ru")
#     segmenter = Segmenter()

#     emb = NewsEmbedding()
#     morph_tagger = NewsMorphTagger(emb)
#     syntax_parser = NewsSyntaxParser(emb)

#     doc = Doc(text)

#     doc.segment(segmenter)
#     doc.tag_morph(morph_tagger)
#     doc.parse_syntax(syntax_parser)

#     massive = []
#     for sent in doc.sents:
#         syntax = sent.syntax
#         for token in syntax.tokens:
#             p = morph.parse(token.text)[0]
#             if (p.normal_form == "кошка"):
#                 text = ""
#                 hasAmod = False
#                 headId = token.id
#                 for token2 in syntax.tokens:
#                     p = morph.parse(token2.text)[0]
#                     if ((token2.head_id == headId or token2.id == headId) and (
#                             token2.rel == "amod" or p.normal_form == "кошка")):
#                         text = text + f"{token2.text} "
#                         if (token2.rel == "amod"):
#                             hasAmod = True
#                 if hasAmod:
#                     massive += [text.strip()]
#     return " ".join(massive)


# def get_list_sentences(fileName):
#     with open(fileName, "r", encoding="utf-8") as file:
#         sentences = []
#         text = file.read()
#         segmenter = Segmenter()
#         doc = Doc(text)
#         doc.segment(segmenter)
#         for i in doc.sents:
#             for j in i.tokens:
#                     sentences += [re.sub(r'[^\w\s]', '', i.text.lower())]
#         return sentences