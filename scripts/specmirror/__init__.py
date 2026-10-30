"""SpecMirror: deterministic Markdown mirrors of font specifications.

SpecMirror downloads a documentation site once, records that download as a
canonical snapshot, and turns the snapshot into a committed Markdown mirror
under ``docs/references/<source>/``. The build stage never reaches the
network, so the same snapshot always yields the same bytes.

The pipeline has three stages.

``fetch pages``
    Reads the discovery index of a source, downloads every page in scope, and
    writes the canonical page plan.
``fetch images``
    Reads the page plan, downloads every image that the pages reference, and
    writes the canonical manifest.
``build``
    Reads the manifest, renders the Markdown mirror, validates the rendered
    tree, and publishes it over the committed output.
"""

__version__ = "0.1.0"
