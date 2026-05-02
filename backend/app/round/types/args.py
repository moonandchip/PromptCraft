from dataclasses import dataclass


@dataclass
class SubmitRoundArgs:
    round_id: str
    user_prompt: str
    # user_id / user_email are None for guest submissions (no persistence).
    user_id: str | None = None
    user_email: str | None = None
    user_display_name: str | None = None


@dataclass
class StartRoundArgs:
    # user_id / user_email are None for guest starts (no persistence).
    user_id: str | None = None
    user_email: str | None = None
    user_display_name: str | None = None
    difficulty: str | None = None
