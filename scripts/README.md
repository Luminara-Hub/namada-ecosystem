# user-and-dev-tools Json to Markdown

This script iterates through the `user-and-dev-tools/{testnet|mainnet}` directories and generates a corresponding markdown file from 
each json file (placing them in a subdirectory `MD`).

By default, all json files and all keys in the json files are included. You can exclude keys from a file, or the entire file, by editing 
`files_keys_exclude.json`, for example:

```
{
  "explorers.json": ["Short Description", "GitHub Account"],
  "masp-indexers.json": ["*"]
}
```
Will omit the given keys/values from `explorers.md`, and will skip generating `masp-indexers.md` entirely.