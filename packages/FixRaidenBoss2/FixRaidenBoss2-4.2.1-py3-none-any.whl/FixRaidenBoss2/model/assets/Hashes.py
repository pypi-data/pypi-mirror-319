##### Credits

# ===== Anime Game Remap (AG Remap) =====
# Authors: NK#1321, Albert Gold#2696
#
# if you used it to remap your mods pls give credit for "Nhok0169" and "Albert Gold#2696"
# Special Thanks:
#   nguen#2011 (for support)
#   SilentNightSound#7430 (for internal knowdege so wrote the blendCorrection code)
#   HazrateGolabi#1364 (for being awesome, and improving the code)

##### EndCredits


##### ExtImports
from typing import Optional, Set, Dict
##### EndExtImports

##### LocalImports
from ...data.HashData import HashData
from .ModIdAssets import ModIdAssets
##### EndLocalImports


##### Script
class Hashes(ModIdAssets):
    """
    This class inherits from :class:`ModDictStrAssets`
    
    Class for managing hashes for a mod

    Parameters
    ----------
    map: Optional[Dict[:class:`str`, Set[:class:`str`]]]
        The `adjacency list`_  that maps the hashes to fix from to the hashes to fix to using the predefined mods :raw-html:`<br />` :raw-html:`<br />`

        **Default**: ``None``
    """

    def __init__(self, map: Optional[Dict[str, Set[str]]] = None):
        super().__init__(HashData, map = map)
##### EndScript
