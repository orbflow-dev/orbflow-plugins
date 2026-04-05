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

## Contributing a Plugin

1. Fork this repository
2. Create your plugin directory under `{language}/{your-name}/{plugin-name}/`
3. Add an `orbflow-plugin.json` manifest ([see format](https://github.com/orbflow-dev/orbflow-python/blob/main/README.md#plugin-manifest))
4. Add your entry to `plugins.json`
5. Open a pull request

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

### Supported Languages

- **Python** — use [orbflow-sdk](https://github.com/orbflow-dev/orbflow-python) (`pip install orbflow-sdk`)
- **TypeScript** — use [@orbflow/sdk](https://github.com/orbflow-dev/orbflow-typescript) (`npm install @orbflow/sdk`)

## Acknowledgements

The `unsloth` plugin collection was adapted from [Unsloth Studio](https://unsloth.ai/docs/new/studio)'s Data Recipe nodes. Thanks to the [Unsloth team](https://github.com/unslothai) for their work on open-source local AI training.

## License

Each plugin is licensed individually (see each plugin's manifest). The repository structure and registry are licensed under [Apache-2.0](LICENSE).
