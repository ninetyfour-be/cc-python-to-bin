"""Sphinx configuration."""
import sys
sys.path.insert(0, "..")


project = "Python binary"
author = "Ninety Four"
copyright = "{% now 'utc', '%Y' %}, Ninety Four"
extensions = [
    "myst_parser",
    "rinoh.frontend.sphinx",
]
rinoh_documents = [
    dict(
        doc="index",
        target=f"ninetyfour",
        title=project,
        subtitle=f"Read me",
        date="",
        domain_indices=False,
        template="template.rtt",
    ),
]
