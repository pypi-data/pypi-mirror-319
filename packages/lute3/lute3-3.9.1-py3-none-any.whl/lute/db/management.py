"""
Db management.
"""

import os
from sqlalchemy import text
from flask import current_app
from lute.models.setting import UserSetting
from lute.models.repositories import UserSettingRepository


def delete_all_data(session):
    """
    DANGEROUS!  Delete everything, restore user settings, clear sys settings.

    NO CHECKS ARE PERFORMED.
    """

    # Setting the pragma first ensures cascade delete.
    statements = [
        "pragma foreign_keys = ON",
        "delete from languages",
        "delete from tags",
        "delete from tags2",
        "delete from settings",
    ]
    for s in statements:
        session.execute(text(s))
    session.commit()
    add_default_user_settings(session, current_app.env_config.default_user_backup_path)


def _revised_mecab_path(repo):
    """
    Change the mecab_path if it's not found, and a
    replacement is found.

    Lute Docker images are built to be multi-arch, and
    interestingly (annoyingly), mecab libraries are installed into
    different locations depending on the architecture, even with
    the same Dockerfile and base image.

    Returns: new mecab path if old one is missing _and_
    new one found, otherwise just return the old one.
    """

    mp = repo.get_value("mecab_path")
    if mp is not None and os.path.exists(mp):
        return mp

    # See develop docs for notes on how to find the libmecab path!
    candidates = [
        # linux/arm64
        "/lib/aarch64-linux-gnu/libmecab.so.2",
        # linux/amd64
        "/lib/x86_64-linux-gnu/libmecab.so.2",
        # github CI, ubuntu-latest
        "/lib/x86_64-linux-gnu/libmecab.so.2",
    ]
    replacements = [p for p in candidates if os.path.exists(p)]
    if len(replacements) > 0:
        return replacements[0]
    # Replacement not found, leave current value as-is.
    return mp


def add_default_user_settings(session, default_user_backup_path):
    """
    Load missing user settings with default values.
    """
    repo = UserSettingRepository(session)

    # These keys are rendered into the global javascript namespace var
    # LUTE_USER_SETTINGS, so if any of these keys change, check the usage
    # of that variable as well.
    keys_and_defaults = {
        "backup_enabled": True,
        "backup_auto": True,
        "backup_warn": True,
        "backup_dir": default_user_backup_path,
        "backup_count": 5,
        "lastbackup": None,
        "mecab_path": None,
        "japanese_reading": "hiragana",
        "current_theme": "-",
        "custom_styles": "/* Custom css to modify Lute's appearance. */",
        "show_highlights": True,
        "current_language_id": 0,
        # Behaviour:
        "open_popup_in_new_tab": False,
        "stop_audio_on_term_form_open": True,
        "stats_calc_sample_size": 5,
        # Term popups:
        "term_popup_promote_parent_translation": True,
        "term_popup_show_components": True,
        # Keyboard shortcuts.  These have default values assigned
        # as they were the hotkeys defined in the initial Lute
        # release.
        "hotkey_Bookmark": "KeyB",
        "hotkey_CopyPara": "shift+KeyC",
        "hotkey_CopySentence": "KeyC",
        "hotkey_NextTheme": "KeyM",
        "hotkey_NextWord": "ArrowRight",
        "hotkey_PrevWord": "ArrowLeft",
        "hotkey_SaveTerm": "ctrl+Enter",
        "hotkey_StartHover": "Escape",
        "hotkey_Status1": "Digit1",
        "hotkey_Status2": "Digit2",
        "hotkey_Status3": "Digit3",
        "hotkey_Status4": "Digit4",
        "hotkey_Status5": "Digit5",
        "hotkey_StatusDown": "ArrowDown",
        "hotkey_StatusIgnore": "KeyI",
        "hotkey_StatusUp": "ArrowUp",
        "hotkey_StatusWellKnown": "KeyW",
        "hotkey_ToggleFocus": "KeyF",
        "hotkey_ToggleHighlight": "KeyH",
        "hotkey_TranslatePara": "shift+KeyT",
        "hotkey_TranslateSentence": "KeyT",
        # New hotkeys.  These must have empty values, because
        # users may have already setup their hotkeys, and we can't
        # assume that a given key combination is free:
        "hotkey_CopyPage": "",
        "hotkey_DeleteTerm": "",
        "hotkey_EditPage": "",
        "hotkey_TranslatePage": "",
        "hotkey_PrevUnknownWord": "",
        "hotkey_NextUnknownWord": "",
        "hotkey_PrevSentence": "",
        "hotkey_NextSentence": "",
    }
    for k, v in keys_and_defaults.items():
        if not repo.key_exists(k):
            s = UserSetting()
            s.key = k
            s.value = v
            session.add(s)
    session.commit()

    # Revise the mecab path if necessary.
    # Note this is done _after_ the defaults are loaded,
    # because the user may have already loaded the defaults
    # (e.g. on machine upgrade) and stored them in the db,
    # so we may have to _update_ the existing setting.
    revised_mecab_path = _revised_mecab_path(repo)
    repo.set_value("mecab_path", revised_mecab_path)
    session.commit()
