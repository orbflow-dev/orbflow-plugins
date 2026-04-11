# Orbflow Community Plugins

Official and community-contributed plugins for [Orbflow](https://github.com/orbflow-dev/orbflow).

The Orbflow marketplace reads `plugins.json` from this repository to discover and list available plugins.

## Structure

```
python/
├── orbflow/              # Reserved for official Orbflow plugins
      ...
├── unsloth/              # Plugins adapted from Unsloth Studio
│   ├── unsloth-uuid-gen/
│   ├── unsloth-ai-codegen/
│   └── ...

typescript/
└── orbflow/              # Official TypeScript plugins
    └── ...
```

Plugins are organized by **language** and **author**. Each plugin is a self-contained directory with:

- `main.py` or `main.ts` — entry point
- `orbflow-plugin.json` — plugin manifest (required)
- `__main__.py` — allows `python -m plugin_name` (Python only)

## Available Plugins

### Unsloth

| Plugin | Category | Description |
|--------|----------|-------------|
| [unsloth-uuid-gen](python/unsloth/unsloth-uuid-gen) | utility | Generate UUID v4 identifiers |
| [unsloth-csv-reader](python/unsloth/unsloth-csv-reader) | data-source | Parse CSV, JSON, and JSONL data |
| [unsloth-code-validator](python/unsloth/unsloth-code-validator) | validation | Validate code syntax |
| [unsloth-random-data](python/unsloth/unsloth-random-data) | utility | Generate random test data |
| [unsloth-schema-transform](python/unsloth/unsloth-schema-transform) | data-processing | Reshape data with field mapping |
| [unsloth-doc-parser](python/unsloth/unsloth-doc-parser) | data-source | Split text into chunks for RAG |
| [unsloth-ai-codegen](python/unsloth/unsloth-ai-codegen) | ai | Generate code using an LLM |
| [unsloth-ai-judge](python/unsloth/unsloth-ai-judge) | ai | Score content using an LLM |
| [unsloth-hf-dataset](python/unsloth/unsloth-hf-dataset) | data-source | Load HuggingFace Hub datasets |

## Plugin SDK

Write your own plugins using the official SDKs:

| SDK | Repository | Package |
|-----|------------|---------|
| Python | [orbflow-dev/orbflow-python](https://github.com/orbflow-dev/orbflow-python) | `pip install orbflow-sdk` |
| TypeScript | [orbflow-dev/orbflow-typescript](https://github.com/orbflow-dev/orbflow-typescript) | `npm install @orbflow/sdk` |

## Publishing to the Registry

Orbflow installs community plugins from a pinned git ref and verifies a SHA-256 checksum for the exact tarball it downloads. Those two fields live in `plugins.json`, not in `orbflow-plugin.json`.

### Recommended: automated publish action

Add this workflow to `.github/workflows/publish.yml` in your plugin repository:

```yaml
name: Publish to Orbflow Registry
on:
  push:
    tags: ["v*"]

permissions:
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: orbflow-dev/publish-plugin-action@v1
        with:
          token: ${{ secrets.ORBFLOW_PUBLISH_TOKEN }}
```

When you push a version tag, the action reads your plugin manifest, computes the tarball checksum for that tag, and opens a PR against `plugins.json` with the generated `git_ref` and `checksum`.

### Manual submission

1. Fork this repository
2. Create your plugin directory under `{language}/{your-name}/{plugin-name}/`
3. Add an `orbflow-plugin.json` manifest ([see format](https://github.com/orbflow-dev/orbflow-python/blob/main/README.md#plugin-manifest))
4. Add or update your entry in `plugins.json`
5. Open a pull request

Manual `plugins.json` entries should include the repository, optional monorepo path, a pinned `git_ref`, and the SHA-256 checksum for the exact archive resolved from that repo and ref:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What it does",
  "author": "Your Name",
  "language": "python",
  "protocol": "grpc",
  "node_types": ["plugin:my-action"],
  "repo": "your-org/your-plugin",
  "path": "plugins/my-plugin",
  "git_ref": "v1.0.0",
  "checksum": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

### Plugin Manifest

Every plugin must include an `orbflow-plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What it does",
  "author": "Your Name",
  "license": "MIT",
  "language": "python",
  "protocol": {
    "Grpc": { "default_port": 50051 }
  },
  "node_types": ["plugin:my-action"],
  "category": "utility",
  "icon": "zap",
  "tags": ["tag1", "tag2"]
}
```

`orbflow-plugin.json` is the runtime manifest used by Orbflow after installation. Do not add `git_ref` or `checksum` to that file; those belong only in the registry entry.

### Supported Languages

- **Python** — use [orbflow-sdk](https://github.com/orbflow-dev/orbflow-python) (`pip install orbflow-sdk`)
- **TypeScript** — use [@orbflow/sdk](https://github.com/orbflow-dev/orbflow-typescript) (`npm install @orbflow/sdk`)

## Acknowledgements

The `unsloth` plugin collection was adapted from [Unsloth Studio](https://unsloth.ai/docs/new/studio)'s Data Recipe nodes. Thanks to the [Unsloth team](https://github.com/unslothai) for their work on open-source local AI training.

## License

Each plugin is licensed individually (see each plugin's manifest). The repository structure and registry are licensed under [Apache-2.0](LICENSE).
