"""Rebuild authored Markdown dossiers and comparison tables from frozen evidence.

This overwrites research/projects/*.md; edit the dossiers_*.py authoring sources
before rebuilding. It does not refresh remote facts or execute reference code.
"""
import dossiers_remix
import dossiers_apps
import dossiers_engines
import dossiers_packaging
import dossiers_frontends
import dossiers_baselines
from research_tools import finish

if __name__ == '__main__':
    for module in [dossiers_remix, dossiers_apps, dossiers_engines,
                   dossiers_packaging, dossiers_frontends, dossiers_baselines]:
        module.write()
    finish()
