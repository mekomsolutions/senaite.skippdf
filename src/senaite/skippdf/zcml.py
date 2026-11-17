"""Environment-controlled ZCML feature registration."""

import os


def provide_skip_pdf_feature(_context):
    """Enable the override only for the explicit process setting ``true``."""
    if os.environ.get("SENAITE_SKIP_PDF", "false") == "true":
        _context.provideFeature("senaite-skip-pdf")
