from pathlib import Path

from mutalyzer_hgvs_parser import author, copyright, project, release

# Generate a single combined grammar file for download from the documentation.
_ebnf_dir = Path(__file__).parent.parent / "mutalyzer_hgvs_parser" / "ebnf"
_grammar_files = ["top.g", "dna.g", "protein.g", "reference.g", "common.g"]
_combined = "\n\n".join((_ebnf_dir / f).read_text() for f in _grammar_files)
(Path(__file__).parent / "hgvs_mutalyzer.g").write_text(_combined)

autoclass_content = 'both'
exclude_patterns = ['_build']
extensions = ['sphinx.ext.autodoc', 'sphinxarg.ext']
root_doc = 'index'
