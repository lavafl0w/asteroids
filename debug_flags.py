"""Tracked debug flag defaults.

Keep the project's normal/default debug values in this file.
If you want personal local-only changes, put them in `debug_flags_local.py`.
That local file is gitignored, so you can flip flags there without polluting commits.
"""

# Project defaults live here.
debug_dict = {
    "DISABLE_PLAYER_ASTEROID_HIT": False,
    "ONLY_DRAW_SINGLE_ASTEROID": False
    }

try:
    # Try to import a local override module.
    # If the file exists, its values can replace the defaults above.
    import debug_flags_local as _local_debug_flags
except ImportError:
    # No local file is totally fine. We just keep the defaults from this file.
    _local_debug_flags = None
    

def _get_flag(name: str, default: bool) -> bool:
    """Return the local override for a flag if it exists, otherwise the default.
    
    Default in this case would be the value of the already predefined project default variable.

    The leading underscore in `_get_flag` and `_local_debug_flags` is just a Python
    convention meaning "internal helper for this module".
    """

    # Module doesn't exist, return default value (which is what it already was)
    if _local_debug_flags is None:
        return default

    # `getattr(module, name, default)` means:
    # "read name (the flag name) from that module (_local_debug_flags), but if it doesn't exist, use default instead."
    return getattr(_local_debug_flags, name, default)


# Check if the flag exists in the dictionary and return the value
def check(flag) -> bool:
    try:
        return debug_dict[flag]
    except KeyError:
        raise KeyError(f"debug flag doesn't exist -> {flag}")

# Re-assign each public flag so local overrides win when present.
for k in debug_dict.keys():
    debug_dict[k] = _get_flag(k, debug_dict[k])
    
# Example is DISABLE_PLAYER_ASTEROID_HIT currently = False
# We try get the value of _get_flag(name) (which checks it from getattr(_local_debug_flags))
# and if _local_debug_flags is none, it returns default (which is itself)
# if the flag isn't in the local file, it also returns default
