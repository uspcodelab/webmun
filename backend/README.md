# Backend folder

Prerequisites: uv

This project uses `uv` for package and project management. Ensure you have it installed. Via curl:
```bash 
curl -LsSf https://astral.sh/uv/install.sh | sh
```

# Setup 

`uv` automatically creates a virtual environment and install dependencies based on the `pyproject.toml`, for this, use:
```bash
uv sync
```

Then, to run development server:

```bash
uv run fastapi dev
```

# Linter & Formatter

Backend uses `ruff` for linter and code formatting. See more at [Ruff Docs](https://docs.astral.sh/ruff/). 

To format code: 

```bash 
uv run ruff format . # replace . with the directory you want to format 
```

To lint & check code for errors:

```bash 
uv run ruff check .
```

# Testing

This project borrows ideas from Test-Driven Development. In particular, try to create tests for a new functionality, and only then try to code it.
To run the test suite:

```bash
uv run pytest
```

We deeply recommend contributers to first lint and test their code before sending the commit. This way we make our codebase better. 

## Realtime resolution voting events

Resolution-related motions use delegation-supplied `resolution_id`,
`amendment_id`, and `split_resolution_id`, along with `resolution_title`,
`target_resolution_id`, `is_friendly`, and `split_title` as applicable. The server
derives the submitting representation and accepts a draft before it enters state.
Once debate ends, the chair starts the first `DRAFT` item in `draft_resolutions`
with `StartResolutionVoteEvent {}`. Pending unfriendly amendments are voted
procedurally before substantive voting begins.

For substantive votes, delegates use `CastVoteEvent { vote }`; chairs can record
a vote with `RecordSubstantiveVoteEvent { representation_id, vote }`. Chairs close
ordinary substantive votes with `CloseSubstantiveVotingEvent`. Roll-call votes use
`AdvanceSubstantiveVoteRoundEvent` for the initial, yes-with-rights, and
no-with-rights rounds; right-of-reply speakers are served through the existing
`NextSpeakerEvent` or `GrantFloorEvent` controls for 30 seconds each.
