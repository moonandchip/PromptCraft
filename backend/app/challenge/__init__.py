"""Challenge module: daily/weekly featured rounds with attempt limits and a leaderboard.

Endpoints:
  GET  /challenge/current      - active challenge plus the caller's progress.
  POST /challenge/submit       - submit a prompt against the active challenge (rate-limited).
  GET  /challenge/leaderboard  - top scores for the active challenge.
"""

from .transport.router import router

__all__ = ["router"]
