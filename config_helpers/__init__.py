# config_helpers/__init__.py
# This file makes config_helpers a proper Python package
# Import all helper functions here for easy access

from .general import (
    read_config_key,
    write_config_key,
    toggle_config_key,
    validate_and_write_numeric,
)
from .blacklist import (
    check_blacklist,
    add_blacklisted_word,
    remove_blacklisted_word,
    get_blacklisted_words,
    add_blacklisted_link,
    remove_blacklisted_link,
    check_scam_links,
)
from .bans import (
    add_to_last_bans,
    remove_from_last_bans,
    get_last_bans,
    remove_ban
)
from .warns import (
    add_warn,
    remove_user_warn_data,
    get_warns,
    clean_non_existent_users
)
from .config_checker import mass_check_json