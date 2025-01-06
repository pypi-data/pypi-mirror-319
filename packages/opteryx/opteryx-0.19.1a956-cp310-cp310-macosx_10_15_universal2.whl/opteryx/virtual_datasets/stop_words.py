# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# See the License at http://www.apache.org/licenses/LICENSE-2.0
# Distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.

"""
Stop Words - words not included in the VECTOR INDEX or in MATCH AGAINST searches
"""

from typing import Set

from orso.schema import FlatColumn
from orso.schema import RelationSchema
from orso.types import OrsoTypes

__all__ = ("read", "schema")

STOP_WORDS: Set[bytes] = {
    b"about",
    b"above",
    b"across",
    b"after",
    b"afterwards",
    b"again",
    b"against",
    b"all",
    b"almost",
    b"alone",
    b"along",
    b"already",
    b"also",
    b"although",
    b"always",
    b"am",
    b"among",
    b"amongst",
    b"amount",
    b"an",
    b"and",
    b"another",
    b"any",
    b"anyhow",
    b"anyone",
    b"anything",
    b"anyway",
    b"anywhere",
    b"are",
    b"around",
    b"as",
    b"at",
    b"back",
    b"be",
    b"became",
    b"because",
    b"become",
    b"becomes",
    b"becoming",
    b"been",
    b"before",
    b"beforehand",
    b"behind",
    b"being",
    b"below",
    b"beside",
    b"besides",
    b"between",
    b"beyond",
    b"both",
    b"bottom",
    b"but",
    b"by",
    b"ca",
    b"call",
    b"can",
    b"cannot",
    b"could",
    b"did",
    b"do",
    b"does",
    b"doing",
    b"done",
    b"down",
    b"due",
    b"during",
    b"each",
    b"eight",
    b"either",
    b"eleven",
    b"else",
    b"elsewhere",
    b"empty",
    b"enough",
    b"even",
    b"ever",
    b"every",
    b"everyone",
    b"everything",
    b"everywhere",
    b"except",
    b"few",
    b"fifteen",
    b"fifty",
    b"first",
    b"five",
    b"for",
    b"former",
    b"formerly",
    b"forty",
    b"four",
    b"from",
    b"front",
    b"full",
    b"further",
    b"get",
    b"give",
    b"go",
    b"had",
    b"has",
    b"have",
    b"he",
    b"hence",
    b"her",
    b"here",
    b"hereafter",
    b"hereby",
    b"herein",
    b"hereupon",
    b"hers",
    b"herself",
    b"him",
    b"himself",
    b"his",
    b"how",
    b"however",
    b"hundred",
    b"if",
    b"in",
    b"indeed",
    b"into",
    b"is",
    b"it",
    b"its",
    b"itself",
    b"just",
    b"keep",
    b"last",
    b"latter",
    b"latterly",
    b"least",
    b"less",
    b"ll",
    b"made",
    b"make",
    b"many",
    b"may",
    b"me",
    b"meanwhile",
    b"might",
    b"mine",
    b"more",
    b"moreover",
    b"most",
    b"mostly",
    b"move",
    b"much",
    b"must",
    b"my",
    b"myself",
    b"name",
    b"namely",
    b"neither",
    b"never",
    b"nevertheless",
    b"next",
    b"nine",
    b"no",
    b"nobody",
    b"none",
    b"noone",
    b"nor",
    b"not",
    b"nothing",
    b"now",
    b"nowhere",
    b"of",
    b"off",
    b"often",
    b"on",
    b"once",
    b"one",
    b"only",
    b"onto",
    b"or",
    b"other",
    b"others",
    b"otherwise",
    b"our",
    b"ours",
    b"ourselves",
    b"out",
    b"over",
    b"own",
    b"part",
    b"per",
    b"perhaps",
    b"please",
    b"put",
    b"quite",
    b"rather",
    b"re",
    b"really",
    b"regarding",
    b"same",
    b"say",
    b"see",
    b"seem",
    b"seemed",
    b"seeming",
    b"seems",
    b"serious",
    b"several",
    b"she",
    b"should",
    b"show",
    b"side",
    b"since",
    b"six",
    b"sixty",
    b"so",
    b"some",
    b"somehow",
    b"someone",
    b"something",
    b"sometime",
    b"sometimes",
    b"somewhere",
    b"still",
    b"such",
    b"take",
    b"ten",
    b"than",
    b"that",
    b"the",
    b"their",
    b"them",
    b"themselves",
    b"then",
    b"thence",
    b"there",
    b"thereafter",
    b"thereby",
    b"therefore",
    b"therein",
    b"thereupon",
    b"these",
    b"they",
    b"third",
    b"this",
    b"those",
    b"though",
    b"three",
    b"through",
    b"throughout",
    b"thru",
    b"thus",
    b"to",
    b"together",
    b"too",
    b"top",
    b"toward",
    b"towards",
    b"twelve",
    b"twenty",
    b"two",
    b"under",
    b"unless",
    b"until",
    b"up",
    b"upon",
    b"us",
    b"used",
    b"using",
    b"various",
    b"very",
    b"via",
    b"ve",
    b"was",
    b"we",
    b"well",
    b"were",
    b"what",
    b"whatever",
    b"when",
    b"whence",
    b"whenever",
    b"where",
    b"whereafter",
    b"whereas",
    b"whereby",
    b"wherein",
    b"whereupon",
    b"wherever",
    b"whether",
    b"which",
    b"while",
    b"whither",
    b"who",
    b"whoever",
    b"whole",
    b"whom",
    b"whose",
    b"why",
    b"will",
    b"with",
    b"within",
    b"without",
    b"would",
    b"yet",
    b"you",
    b"your",
    b"yours",
    b"yourself",
    b"yourselves",
}


def read(end_date=None, *args):
    import pyarrow

    # Define the data
    data = [
        pyarrow.array(
            STOP_WORDS,
            type=pyarrow.string(),
        ),
    ]
    column_names = ["value"]

    return pyarrow.Table.from_arrays(data, column_names)


def schema():
    # fmt:off
    return RelationSchema(
            name="$stop_words",
            columns=[
                FlatColumn(name="value", type=OrsoTypes.VARCHAR),
            ],
        )
    # fmt:on
