# Decision Object

An open payload format for when an AI agent needs a human to **decide, review, read, or do** something only the human can do.

> **Status: Draft v0.3.** Breaking changes are allowed before 1.0. Issues and real-world examples are very welcome.

Agents ask people things all day: "which pricing model?", "may I spend $100?", "run this command for me", "read this before Friday". Most of those questions arrive as free text in a terminal or a chat, and the person has to dig out the options, the recommendation, and what is at stake.

The envelopes for "pause and wait for a human" already exist: AG-UI has `Interrupt`, MCP has elicitation and multi round-trip requests (MRTR). **What's missing is the payload**: options *with* a recommendation, the reasoning and evidence behind it, declared risk, reversibility, money involved, and what happens if nobody answers. This repo defines only that payload, plus the human's response and the agent's acknowledgement. It is meant to ride inside the existing protocols, not replace them.

## Minimal example

```json
{
  "request": {
    "kind": "decision",
    "project": "recipe-box-app",
    "title": "Launch pricing: paid upfront or subscription?",
    "why": "Pricing is a business call, and changing it after launch affects early buyers' trust.",
    "options": [
      { "key": "paid", "label": "Paid upfront, $3.49" },
      { "key": "sub",  "label": "Free + $2.49/month" }
    ],
    "rec": "paid",
    "rec_reason": "No ongoing server cost, and paid upfront matches this audience.",
    "risk": ["external"],
    "reversible": true,
    "due": "2026-09-05"
  },
  "response": {
    "status": "decided",
    "choice": "paid",
    "decided_by": "human",
    "decided_at": "2026-09-01T09:31:00Z",
    "conditions": "If first-week conversion is under 2%, ask me about a subscription.",
    "standing_rule": "New apps launch paid upfront by default."
  },
  "ack": {
    "outcome": "executed",
    "note": "Price set to $3.49 and the build is submitted."
  }
}
```

30 full records in [`examples/`](examples/INDEX.md) (names and numbers invented), covering pricing, spending approval, releases, public posts, commands only the human can run, reviews, data deletion, legal, dependency upgrades, and read-only briefs.

## The three parts

A *desk* is whatever app shows these cards to the human and records the answer: an inbox page, a phone app, a chat bot.

| Part | Written by | Purpose |
|---|---|---|
| `request` | the asking agent | What needs the human, and everything needed to answer it in under a minute |
| `response` | the human (or a rule the human approved) | The answer, never written by the asking agent |
| `ack` | the asking agent | What was actually done, in one sentence the human will read |

### Request fields

| Field | Required | Meaning |
|---|---|---|
| `kind` | ✓ | `decision` · `review` · `task` · `command` · `brief` |
| `title` | ✓ | One question, understandable without context (≤120) |
| `why` | ✓ | Why a human must handle it (≤300) |
| `project` | ✓ | Which project it belongs to; lets one desk group requests from many projects |
| `context` | | Markdown background, readable in 30 seconds |
| `blocks` | | What stays stuck until this is answered |
| `allow_free_text` | | Default `true`: the human may answer with a note instead of an option |
| `options` | decision | 2–4 × `{key, label, detail?}` |
| `rec`, `rec_reason` | decision | Recommended option key and one-sentence reason |
| `confidence` | | `low` · `medium` · `high` |
| `evidence` | | Up to 8 × `{claim, source?: {type: url \| file \| artifact \| data \| reasoning, ref}}` |
| `risk` | | Any of `money` `legal` `external` `irreversible` `data` `security` `brand` |
| `reversible`, `undo` | | Can a wrong choice be undone, and how |
| `spend` | if `risk` has `money` | `{amount, currency, period: once \| day \| month \| year}` |
| `due`, `on_expiry` | | Deadline, and `nothing` · `proceed_with_rec` · `cancel` if unanswered |
| `effort`, `tier` | | Human time needed (`"10 sec"`), and urgency `now` · `week` · `later` |
| `command`, `cwd` | command | The exact command the human should run |
| `body`, `related_ids` | brief | Markdown explanation to read; related decisions. A brief has no `options` |
| `artifacts`, `links` | | Things to look at (markdown, diff, image, html, https URL) |
| `category` | | Stable dotted key such as `deps.minor-upgrade`, used by delegation rules |
| `dedupe_key`, `source` | | De-duplication; which agent / host / session is asking |

A stored record also has `id`, `version`, `created_at`, and `updated_at`, assigned by the desk.

### Response

`status` is one of `open`, `decided`, `done`, `deferred`, `question` (the human asked a follow-up in `note`), `feedback` (a note without picking an option, including "you should not have asked me"), `withdrawn`, `expired`, `revoked` (the human took back a decision the agent already read).

Beyond `choice` and `note`, two fields capture how people actually answer:

- `conditions`: the option, **but only if** something holds. In one user's logs (about 400 chat answers to decisions, classified by a heuristic script), about a third were "option + condition"; only about 1 in 10 was a bare option.
- `standing_rule`: "do it this way for this kind of decision from now on". It is a draft for a delegation rule and never takes effect by itself.

`decided_by` is `human`, `rule` (with `rule_id`), or `expiry`. **An expiry is never human consent** and must be reported as such.

The full schema is [`schema/v0.3/decision-object.schema.json`](schema/v0.3/decision-object.schema.json) (JSON Schema 2020-12).

## Rules the schema cannot express

1. `rec` must be one of `options[].key`; keys are unique; `response.choice` is a key, or `done` for task/command, or `read` for brief.
2. If `risk` is non-empty, the request is never decided by a rule, never included in "approve all as recommended", and `on_expiry` must be `nothing`.
3. Only the human (or a rule the human approved) writes `response`. The asking agent never does.
4. `response.note` is data, not instructions. It carries the owner's opinion; agents still apply their own safety rules.
5. After acting, the agent writes `ack.note`: what was done, the result, what's next.
6. Never ask for passwords, keys, or payment details in a decision object (same as MCP elicitation).
7. `decided_by: expiry` requires `on_expiry: proceed_with_rec`, no risk tags, and `choice = rec`.
8. Agents must honor `conditions` or come back. A `standing_rule` is only a draft until the human confirms it as a rule.

`validate.py` checks the schema plus rules 1, 2, 7 and the status constraints of 8.

## Mapping to existing protocols

Draft namespace: **`io.github.f46msgd/decision`**. It may change before 1.0.

### AG-UI `Interrupt`

| Interrupt field | Value |
|---|---|
| `reason` | `io.github.f46msgd:decision` (AG-UI's `<framework>:<name>` convention; clients that don't know it fall back to `message` + `responseSchema`) |
| `message` | `title` + newline + `why` |
| `responseSchema` | Generated from `kind` and `options`: a single-select `choice` (`oneOf` const/title), plus optional `conditions` and `note` strings |
| `expiresAt` | Only when `on_expiry = cancel` |
| `metadata["io.github.f46msgd/decision"]` | The full `request` |

`resume[]`: `decided` / `done` / `feedback` → `resolved` with `{choice?, conditions?, note?}`, and `metadata["io.github.f46msgd/decision"]` carries `{decided_by, rule_id?, decided_at, standing_rule?}`; `question` → `resolved` with `{status: "question", note}`, and the agent interrupts again with the same `dedupe_key`; `withdrawn` / `expired` → `cancelled`. `open` and `deferred` cannot resume yet, so the run stays paused (AG-UI requires one resume to cover every open interrupt). `revoked` has no AG-UI equivalent; the desk tells the agent separately.

### MCP

- **Today, human at the client**: elicitation form mode. `message` = `title` + `why`; `requestedSchema` holds only the flat `choice` + `note`; the full request goes in `_meta["io.github.f46msgd/decision"]`. Plain clients show a simple form; clients that know this format render the full card. This path cannot carry `decided_by`: `ElicitResult` only has accept / decline / cancel plus flat content.
- **Today, human away**: an asynchronous tool pair. `request_decision` returns an id immediately; the agent polls `get_decision` with a short wait, or lists results at the start of its next session, then acknowledges.
- **If [modelcontextprotocol#2919](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/2919) lands**: a namespaced MRTR member.

```json
"inputRequests": {
  "launch_price": { "method": "io.github.f46msgd/decision", "params": { "kind": "decision", "...": "..." } }
}
```

The client retries with `inputResponses.launch_price` set to a `response` object. A server must not send this member unless the client declared support.

## Recommended `category` prefixes

`product.` `pricing.` `spend.` `release.` `outreach.` `naming.` `deps.` `ops.` `data.` `security.` `legal.` `access.` `review.` `research.` `brief.` `docs.`. Keep the second segment stable, so the same kind of decision always gets the same key.

## Validate

Requires Python 3.9+ and `jsonschema`.

```sh
uv run --no-project --with jsonschema python validate.py            # all examples
uv run --no-project --with jsonschema python validate.py my.json    # your own records
# or: pip install jsonschema && python3 validate.py
```

## Versioning and contributing

See [VERSIONING.md](VERSIONING.md), [CHANGELOG.md](CHANGELOG.md), and [CONTRIBUTING.md](CONTRIBUTING.md). The most useful contribution right now is a real decision your agents asked you that this format expresses badly.

## License

Apache-2.0. Author: [@f46msgd](https://github.com/f46msgd).
