"""Contract tests for the hyper provider profile.

Run from the hermes-agent repo root:
    python3 -m pytest tests/ -x  # repo tests
    python3 tests/test_hyper_profile.py  # these
"""

import os
import sys
from pathlib import Path

# Make the hermes-agent repo importable, then load the plugin the same way
# Hermes' discovery does (exec the plugin dir's __init__ with `providers` importable).
HERMES_REPO = os.environ.get("HERMES_REPO", str(Path.home() / ".hermes/hermes-agent"))
sys.path.insert(0, HERMES_REPO)

import importlib.util  # noqa: E402
import providers  # noqa: E402

_PLUGIN_INIT = Path(__file__).resolve().parent.parent / "hyper" / "__init__.py"


def _load_plugin() -> None:
    if providers.get_provider_profile("hyper") is not None:
        return
    spec = importlib.util.spec_from_file_location("hyper_plugin", _PLUGIN_INIT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


def _profile():
    _load_plugin()
    p = providers.get_provider_profile("hyper")
    assert p is not None, "hyper profile not registered"
    return p


def test_profile_registered_under_all_names():
    p = _profile()
    assert p.name == "hyper"
    for alias in ("charm", "charm-hyper"):
        assert providers.get_provider_profile(alias).name == "hyper"


def test_auth_and_endpoint():
    p = _profile()
    assert p.auth_type == "api_key"
    assert p.env_vars == ("HYPER_API_KEY",)
    assert p.base_url == "https://hyper.charm.land/v1"
    assert p.get_hostname() == "hyper.charm.land"


def test_aux_model_in_catalog():
    """default_aux_model must be a real serving model id (live check)."""
    p = _profile()
    models = p.fetch_models() or ()
    assert p.default_aux_model in models, f"{p.default_aux_model} not in live catalog"


def test_fallback_models_are_real():
    """Every fallback entry must exist in the live catalog (no ghost ids)."""
    p = _profile()
    models = set(p.fetch_models() or ())
    assert p.fallback_models, "fallback_models must not be empty"
    for mid in p.fallback_models:
        assert mid in models, f"fallback model {mid} not in live catalog"


def test_env_key_resolution(tmp_path=None):
    """resolve_runtime_provider must pick the key up from HYPER_API_KEY.

    Uses an isolated HERMES_HOME so the developer's real ~/.hermes/.env
    dotenv value cannot shadow the process-env key this test sets.
    """
    import tempfile

    from hermes_cli.runtime_provider import resolve_runtime_provider

    os.environ["HYPER_API_KEY"] = "sk-hyper-test-placeholder"
    old_home = os.environ.get("HERMES_HOME")
    os.environ["HERMES_HOME"] = tempfile.mkdtemp(prefix="hyper-test-")
    try:
        rt = resolve_runtime_provider(requested="hyper", target_model="glm-5.3-flash")
        assert rt["base_url"] == "https://hyper.charm.land/v1"
        assert rt["api_mode"] == "chat_completions"
        assert rt["api_key"].startswith("sk-hyper-test")
    finally:
        os.environ.pop("HYPER_API_KEY", None)
        if old_home is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = old_home


if __name__ == "__main__":
    test_profile_registered_under_all_names()
    test_auth_and_endpoint()
    test_aux_model_in_catalog()
    test_fallback_models_are_real()
    test_env_key_resolution()
    print("all hyper profile tests passed")
