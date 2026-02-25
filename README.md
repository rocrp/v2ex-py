# v2ex

CLI client for [V2EX](https://www.v2ex.com) API.

## Install

```bash
uv sync
```

## Setup

Create `.env` in project root:

```
V2EX_TOKEN=your_personal_access_token
```

Get a token at <https://www.v2ex.com/settings/tokens>.

## Usage

```bash
v2ex hot                     # trending topics
v2ex latest                  # latest topics
v2ex node python             # topics in a node
v2ex node python --info      # node metadata
v2ex topic 1234567           # topic detail + replies
v2ex notif                   # notifications
v2ex token                   # token info
v2ex me                      # authenticated user info
```

### Output formats

Default output is rich tables. Use global flags for machine-readable formats:

```bash
v2ex --json hot              # JSON
v2ex --markdown hot          # Markdown (alias: --md)
```
