from dataclasses import dataclass


@dataclass
class SubmitRoundArgs:
    user_email: str
    round_id: str
    user_prompt: str


@dataclass
class StartRoundArgs:
    user_id: str
