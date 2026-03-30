# Orbflow Community Plugins

Official and community-contributed plugins for [Orbflow](https://github.com/orbflow-dev/orbflow).

The Orbflow marketplace reads `plugins.json` from this repository to discover and list available plugins.

## Structure

```
python/
└── orbflow/              # Official plugins by the Orbflow team
    ├── orbflow-uuid-gen/
    ├── orbflow-ai-codegen/
    └── ...

typescript/
└── orbflow/              # Official TypeScript plugins
    └── ...
```

Plugins are organized by **language** and **author**. Each plugin is a self-contained directory with:

- `main.py` or `main.ts` — entry point
- `orbflow-plugin.json` — plugin manifest (required)
- `__main__.py` — allows `python -m plugin_name` (Python only)

## Available Plugins

| Plugin | Category | Language | Description |
|--------|----------|----------|-------------|
| [orbflow-uuid-gen](python/orbflow/orbflow-uuid-gen) | utility | Python | Generate UUID v4 identifiers |
| [orbflow-csv-reader](python/orbflow/orbflow-csv-reader) | data-source | Python | Parse CSV, JSON, and JSONL data |
| [orbflow-code-validator](python/orbflow/orbflow-code-validator) | validation | Python | Validate code syntax |
| [orbflow-random-data](python/orbflow/orbflow-random-data) | utility | Python | Generate random test data |
| [orbflow-schema-transform](python/orbflow/orbflow-schema-transform) | data-processing | Python | Reshape data with field mapping |
| [orbflow-doc-parser](python/orbflow/orbflow-doc-parser) | data-source | Python | Split text into chunks for RAG |
| [orbflow-ai-codegen](python/orbflow/orbflow-ai-codegen) | ai | Python | Generate code using an LLM |
| [orbflow-ai-judge](python/orbflow/orbflow-ai-judge) | ai | Python | Score content using an LLM |
| [orbflow-hf-dataset](python/orbflow/orbflow-hf-dataset) | data-source | Python | Load HuggingFace Hub datasets |

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

## License

Each plugin is licensed individually (see each plugin's manifest). The repository structure and registry are licensed under [Apache-2.0](LICENSE).
