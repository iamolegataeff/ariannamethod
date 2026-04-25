"""api_guard — defensive rate limiter for Anthropic API calls.

Background: this umbrella ecosystem (Ariana, Scribe, Defender, Monday, voice_webhooks,
mac_daemon, linux_defender) leaked roughly $20/day on the Anthropic API for months
on an Intel Mac before being killed. The likely culprit was a launchd daemon with
KeepAlive=true, plus Flask webhooks always-on receiving accidental traffic. To
prevent the same pattern after revival on phone (Termux) or any Linux box, every
anthropic.messages.create call MUST go through this guard.

Usage:
    from api_guard import guarded_messages_create
    response = guarded_messages_create(client, model="...", max_tokens=..., messages=[...])

The guard:
- Persists call timestamps to ~/.arianna_api_guard.jsonl (one JSON line per call).
- Enforces per-process limits AND persistent (cross-process) limits via the file.
- Default caps: 30 calls/hour, 200 calls/day. Override via env vars
  ARIANNA_API_MAX_PER_HOUR / ARIANNA_API_MAX_PER_DAY.
- Hard-blocks (raises RuntimeError) when limits are exceeded — refuse to call
  rather than spend silently.

This is defense-in-depth alongside the disabled launchd plist / systemd service /
launch_all_webhooks.sh — see device-1/finally.md.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

LOG_PATH = Path(os.path.expanduser("~/.arianna_api_guard.jsonl"))
DEFAULT_MAX_PER_HOUR = int(os.environ.get("ARIANNA_API_MAX_PER_HOUR", "30"))
DEFAULT_MAX_PER_DAY = int(os.environ.get("ARIANNA_API_MAX_PER_DAY", "200"))


class ApiGuardLimitExceeded(RuntimeError):
    """Raised when the guard refuses to make a call."""


def _read_recent_calls(window_seconds: int) -> list[float]:
    """Return timestamps of calls within the last `window_seconds`."""
    if not LOG_PATH.exists():
        return []
    now = time.time()
    out: list[float] = []
    try:
        with LOG_PATH.open("r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = float(entry.get("ts", 0))
                except (ValueError, TypeError):
                    continue
                if now - ts < window_seconds:
                    out.append(ts)
    except OSError:
        pass
    return out


def _record_call(model: str, caller: str) -> None:
    """Append a call record to the persistent log."""
    entry = {"ts": time.time(), "model": model, "caller": caller, "pid": os.getpid()}
    try:
        with LOG_PATH.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        # If we can't log, fail closed — don't make the call.
        raise ApiGuardLimitExceeded(
            f"api_guard: cannot write to {LOG_PATH}; refusing to call API"
        )


def check_limits(
    *,
    max_per_hour: int = DEFAULT_MAX_PER_HOUR,
    max_per_day: int = DEFAULT_MAX_PER_DAY,
) -> None:
    """Raise ApiGuardLimitExceeded if recent call counts exceed thresholds."""
    last_hour = len(_read_recent_calls(3600))
    last_day = len(_read_recent_calls(86400))
    if last_hour >= max_per_hour:
        raise ApiGuardLimitExceeded(
            f"api_guard: {last_hour} calls in last hour >= cap {max_per_hour}"
        )
    if last_day >= max_per_day:
        raise ApiGuardLimitExceeded(
            f"api_guard: {last_day} calls in last 24h >= cap {max_per_day}"
        )


def guarded_messages_create(
    client: Any,
    *,
    caller: str = "unknown",
    max_per_hour: int = DEFAULT_MAX_PER_HOUR,
    max_per_day: int = DEFAULT_MAX_PER_DAY,
    **kwargs: Any,
) -> Any:
    """Rate-limited drop-in for `client.messages.create(**kwargs)`.

    Pass the anthropic client (`Anthropic(api_key=...)` or any object with
    `.messages.create`) and call kwargs (model, max_tokens, messages, ...).
    `caller` is a short label like "scribe.py:486" used for log forensics.
    """
    check_limits(max_per_hour=max_per_hour, max_per_day=max_per_day)
    model = kwargs.get("model", "?")
    _record_call(model=model, caller=caller)
    return client.messages.create(**kwargs)


def stats() -> dict[str, int]:
    """Quick check: how many calls in last hour / day."""
    return {
        "last_hour": len(_read_recent_calls(3600)),
        "last_day": len(_read_recent_calls(86400)),
        "cap_per_hour": DEFAULT_MAX_PER_HOUR,
        "cap_per_day": DEFAULT_MAX_PER_DAY,
    }


if __name__ == "__main__":
    import sys

    s = stats()
    print(f"api_guard stats:")
    print(f"  last hour: {s['last_hour']} / {s['cap_per_hour']}")
    print(f"  last 24h:  {s['last_day']} / {s['cap_per_day']}")
    print(f"  log:       {LOG_PATH}")
    sys.exit(0)
