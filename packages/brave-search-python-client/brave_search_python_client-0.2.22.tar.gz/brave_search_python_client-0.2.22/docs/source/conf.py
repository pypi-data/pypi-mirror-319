"""Sphinx configuration."""  # noqa: INP001

import re
from datetime import UTC, datetime

extensions = [
    "sphinx_toolbox.collapse",  # https://sphinx-toolbox.readthedocs.io/
    "sphinx_toolbox.sidebar_links",
    "sphinx_toolbox.github",
    "sphinx_toolbox.source",
    "sphinx.ext.autodoc",
    "enum_tools.autoenum",  # https://github.com/domdfcoding/enum_tools/tree/master
    "sphinx.ext.napoleon",  # https://sphinxcontrib-napoleon.readthedocs.io/en/latest/
    "sphinx-pydantic",
    "sphinxcontrib.autodoc_pydantic",  # https://autodoc-pydantic.readthedocs.io/en/stable/users/examples.html
    "sphinx.ext.coverage",
    "sphinx_copybutton",
    "sphinx.ext.extlinks",  # https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html
    "sphinx.ext.imgconverter",
    "sphinx_inline_tabs",
    "sphinx_mdinclude",
    "sphinxext.opengraph",
]

project = "brave-search-python-client"
author = "Helmut Hoffer von Ankershoffen"
copyright = f" (c) 2025-{datetime.now(UTC).year}, {author}"  # noqa: A001
version = "0.2.22"
release = version
github_username = "helmut-hoffer-von-ankershoffen"
github_repository = "brave-search-python-client"

language = "en"

ogp_site_name = "Brave Search Python Client"
ogp_image = "https://brave-search-python-client.readthedocs.io/en/latest/_static/brave.png"
ogp_custom_meta_tags = [
    '<meta name="twitter:card" content="Brave Search Python Client" />',
]
ogp_enable_meta_description = True
ogp_description_length = 300

autodoc_pydantic_model_show_json = False

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

linkcheck_retries = 2
linkcheck_timeout = 1
linkcheck_workers = 10
linkcheck_ignore = [
    r"http://127\.0\.0\.1",
    r"http://localhost",
]


templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
html_logo = "../../brave.png"
html_theme_options = {
    "announcement": (
        '<a target="_blank" href="https://github.com/helmut-hoffer-von-ankershoffen/brave-search-python-client">GitHub</a> - '  # noqa: E501
        '<a target="_blank" href="https://pypi.org/project/brave-search-python-client/">PyPI</a> - '
        '<a target="_blank" href="https://hub.docker.com/r/helmuthva/brave-search-python-client/tags">Docker</a> - '
        '<a target="_blank" href="https://sonarcloud.io/summary/new_code?id=helmut-hoffer-von-ankershoffen_brave-search-python-client">SonarQube</a> - '  # noqa: E501
        '<a target="_blank" href="https://app.codecov.io/gh/helmut-hoffer-von-ankershoffen/brave-search-python-client">Codecov</a>'
    ),
}

latex_engine = "lualatex"  # https://github.com/readthedocs/readthedocs.org/issues/8382

# If true, show page references after internal links.
latex_show_pagerefs = True

# If true, show URL addresses after external links.
latex_show_urls = "footnote"

# If false, no module index is generated.
latex_domain_indices = True

# See https://www.sphinx-doc.org/en/master/latex.html
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    "papersize": "a4paper",
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "10pt",
    # https://github.com/sphinx-doc/sphinx/issues/12332.
    "preamble": r"""
\directlua {
  luaotfload.add_fallback("emoji",
  {
     "[TwemojiMozilla.ttf]:mode=harf;",
     "[DejaVuSans.ttf]:mode=harf;",
  }
  )
}
\setmainfont{LatinModernRoman}[RawFeature={fallback=emoji},SmallCapsFont={* Caps}]
\setsansfont{LatinModernSans}[RawFeature={fallback=emoji}]
\setmonofont{DejaVuSansMono}[RawFeature={fallback=emoji},Scale=0.8]
    """,
}

slug = re.sub(r"\W+", "-", project.lower())

latex_documents = [
    ("index", f"{slug}.tex", rf"{project} Documentation", author, "manual", False),
]

latex_logo = "../../brave.png"
