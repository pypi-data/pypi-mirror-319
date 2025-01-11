from modelly.themes.base import Base, ThemeClass
from modelly.themes.citrus import Citrus
from modelly.themes.default import Default
from modelly.themes.glass import Glass
from modelly.themes.monochrome import Monochrome
from modelly.themes.ocean import Ocean
from modelly.themes.origin import Origin
from modelly.themes.soft import Soft
from modelly.themes.utils import colors, sizes
from modelly.themes.utils.colors import Color
from modelly.themes.utils.fonts import Font, GoogleFont
from modelly.themes.utils.sizes import Size

__all__ = [
    "Base",
    "Color",
    "Default",
    "Font",
    "Glass",
    "GoogleFont",
    "Monochrome",
    "Size",
    "Soft",
    "ThemeClass",
    "colors",
    "sizes",
    "Origin",
    "Citrus",
    "Ocean",
]


def builder(*args, **kwargs):
    from modelly.themes.builder_app import demo

    return demo.launch(*args, **kwargs)
