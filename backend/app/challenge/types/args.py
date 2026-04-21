from dataclasses import dataclass


@dataclass
class GetCurrentChallengeArgs:
    user_id: str


@dataclass
class SubmitChallengeArgs:
    user_id: str
    user_email: str
    user_prompt: str
    user_display_name: str | None = None


@dataclass
class GetLeaderboardArgs:
    limit: int
