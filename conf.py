extensions = ['sphinxcontrib.bibtex','sphinx.ext.mathjax']
master_doc = 'index'
project = u'Project documentations'
copyright = u'Public'
author = u'-'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
# latex_documents = [
#    (master_doc, 'oemof_heat.tex', u'oemof\\_heat Documentation',
#     u'c-moeller, jnnr', 'manual'),
# ]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'oemof_heat', u'oemof_heat Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'oemof_heat', u'oemof_heat Documentation',
     author, 'oemof_heat', 'One line description of project.',
     'Miscellaneous'),
]
