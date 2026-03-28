from dataclasses import dataclass


@dataclass
class SubmitRoundArgs:
    user_id: str
    user_email: str
    round_id: str
    user_prompt: str
    user_display_name: str | None = None


@dataclass
class StartRoundArgs:
    user_id: str
    user_email: str
    user_display_name: str | None = None
