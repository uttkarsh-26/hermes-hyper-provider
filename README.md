# hyper — Charm Hyper model-provider plugin for Hermes Agent

Standalone [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin that adds
[Charm Hyper](https://hyper.charm.land) as a first-class provider profile.

Hyper is fast, cost-effective OpenAI-compatible inference built for agentic coding:
31 hand-picked models (GLM-5.3, DeepSeek V4, Kimi K3, Qwen3.8, ...), a public model
catalog with context/pricing metadata, and per-model reasoning-effort control.

## Install

```bash
git clone https://github.com/uttkarsh-26/hermes-hyper-provider.git
mkdir -p ~/.hermes/plugins/model-providers
cp -r hermes-hyper-provider/hyper ~/.hermes/plugins/model-providers/hyper
```

Then set your key in `~/.hermes/.env` (get one at [hyper.charm.land](https://hyper.charm.land) — keys start with `sk-hyper-`):

```bash
HYPER_API_KEY=sk-hyper-xxxxxxxxxxxxxxxx
```

Start a new Hermes session and run `hermes model` — **Charm Hyper** appears in the
provider list with the full live catalog. `/model hyper` switches to it; the
`charm` and `charm-hyper` aliases work too.

## What auto-wires

| Surface | Behavior |
|---|---|
| `hermes model` / `/model` picker | Hyper row with all 31 models, fetched live from the public `https://hyper.charm.land/v1/models` |
| Runtime resolution | `--provider hyper` / `/model hyper/<model>` route through the standard API-key path |
| Context lengths | Resolved from models.dev via the `hyper.charm.land` base-URL match (all models 1M-2^20 tokens) |
| Pricing display | From the same models.dev catalog |
| Auxiliary tasks | `glm-5.3-flash` pinned as the default aux model (cheapest capable model, vision-capable) |
| Credential pool | `HYPER_API_KEY` picked up from `.env` automatically |

## Model catalog

The live `/v1/models` endpoint is the source of truth (no auth needed, carries
context windows and pricing for every model). If the live fetch fails, the picker
falls back to a static list of four broadly useful agent models:
`glm-5.3-flash`, `deepseek-v4.1-flash`, `glm-5.3`, `kimi-k3`.

## Reasoning effort

Reasoning models on Hyper accept `reasoning_effort` (`low`/`high`/`max` on the GLM
and Kimi families). Set it per-use-case in `config.yaml`, e.g.:

```yaml
agent:
  reasoning_effort: high
```

## Uninstall

```bash
rm -rf ~/.hermes/plugins/model-providers/hyper
```

## Why standalone

Per NousResearch/hermes-agent's `in-tree-provider-integration` policy
(`AGENTS.md`), third-party provider integrations ship as standalone plugin repos
rather than in-tree directories. This repo follows that policy; the same plugin
layout also works in-tree for local installs.

## License

MIT
