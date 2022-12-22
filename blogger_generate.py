# Copyright (c) 2022-present AuthorAI.org (authorai.org@gmail.com)

from authorai import blogger
import sys

if len(sys.argv) == 1:
    keywords = ['Physics', 'Art', 'City']
else:
    keywords = sys.argv[1 : None]

blogger.auto_generate(keywords=keywords, verbose=True, folder='generated')

