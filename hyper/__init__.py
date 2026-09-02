"""Charm Hyper provider profile.

Hyper (hyper.charm.land) is a fast, cost-effective OpenAI-compatible
inference service built for agentic coding. Chat inference is served from
``https://hyper.charm.land/v1`` with standard Bearer auth and the model
catalog is published publicly at ``/v1/models`` (no auth required).

Standalone plugin — distributed per NousResearch/hermes-agent's
in-tree-provider-integration policy (see AGENTS.md). Install by dropping
this directory at ``$HERMES_HOME/plugins/model-providers/hyper/`` (see
README.md).
"""

from providers import register_provider
from providers.base import ProviderProfile

hyper = ProviderProfile(
    name="hyper",
    aliases=("charm", "charm-hyper"),
    display_name="Charm Hyper",
    description="Charm Hyper — OpenAI-compatible inference for agentic coding",
    signup_url="https://hyper.charm.land",
    env_vars=("HYPER_API_KEY",),
    base_url="https://hyper.charm.land/v1",
    auth_type="api_key",
    # glm-5.3-flash is the cheapest capable model (vision-capable, 1M context);
    # aux resolution is synchronous, so one model is pinned here.
    default_aux_model="glm-5.3-flash",
    # The live ``/v1/models`` endpoint is public and carries context/pricing
    # metadata for all 31 models, so it is the catalog source of truth.
    # ``fallback_models`` only shows in the /model picker when the live fetch
    # fails — keep it to the four broadly-useful agents' models.
    fallback_models=(
        "glm-5.3-flash",
        "deepseek-v4-flash",
        "glm-5.3",
        "kimi-k3",
    ),
)

register_provider(hyper)
