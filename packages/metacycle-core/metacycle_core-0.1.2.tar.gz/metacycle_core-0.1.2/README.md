# Development

```
uv sync
```

# Run

```
uv run metacycle-hello
```

# Upload to PyPI and then run as as a tool
This is how end users will run the server in a single line.

```
rm -r dist/
uv build
uv publish --token $TOKEN
```

Open another terminal:
```
uvx --from metacycle-core@latest metacycle-hello
```