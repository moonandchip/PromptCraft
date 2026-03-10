"""Data layer: persist a round submission (prompt + attempt) to PostgreSQL."""
import logging
import uuid

log = logging.getLogger(__name__)

_DIFFICULTY_TO_LEVEL: dict[str, int] = {"easy": 1, "medium": 3, "hard": 5}


def get_or_create_user(conn, email: str, username: str | None = None) -> str:
    """Return the public-schema UUID for a user, inserting a row if not present.

    The auth service stores users with cuid PKs in its own schema.  We keep a
    mirror row in the public `users` table keyed by email so that attempts and
    prompts can reference a proper UUID.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email = %s LIMIT 1", (email,))
        row = cur.fetchone()
        if row:
            return str(row[0])

        new_id = str(uuid.uuid4())
        display_name = username or email.split("@")[0]
        cur.execute(
            """
            INSERT INTO users (id, username, email, password_hash, created_at, total_score, role)
            VALUES (%s, %s, %s, '', NOW(), 0, 'user')
            ON CONFLICT (email) DO NOTHING
            RETURNING id
            """,
            (new_id, display_name, email),
        )
        row = cur.fetchone()
        # If another concurrent insert won the race, fetch the existing row.
        if row is None:
            cur.execute("SELECT id FROM users WHERE email = %s LIMIT 1", (email,))
            row = cur.fetchone()
        return str(row[0])


def get_or_create_image(conn, reference_image: str, difficulty: str) -> str:
    """Return the DB UUID for a reference image, inserting a row if not present.

    Matches by image_url containing the reference_image filename so that
    images seeded with a full path (e.g. /static/ancient-temple.jpg) are
    also found.
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM images WHERE image_url LIKE %s LIMIT 1",
            (f"%{reference_image}%",),
        )
        row = cur.fetchone()
        if row:
            return str(row[0])

        new_id = str(uuid.uuid4())
        difficulty_level = _DIFFICULTY_TO_LEVEL.get(difficulty, 3)
        cur.execute(
            """
            INSERT INTO images (id, image_url, difficulty_level, created_at, is_active)
            VALUES (%s, %s, %s, NOW(), TRUE)
            RETURNING id
            """,
            (new_id, reference_image, difficulty_level),
        )
        return str(cur.fetchone()[0])


def save_prompt(conn, user_id: str, image_id: str, prompt_text: str) -> str:
    """Insert a prompt row and return its new UUID."""
    with conn.cursor() as cur:
        new_id = str(uuid.uuid4())
        cur.execute(
            """
            INSERT INTO prompts (id, user_id, image_id, prompt_text, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            RETURNING id
            """,
            (new_id, user_id, image_id, prompt_text),
        )
        return str(cur.fetchone()[0])


def _get_attempt_number(conn, user_id: str, image_id: str) -> int:
    """Return the next 1-based attempt number for this user/image pair."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM attempts WHERE user_id = %s AND image_id = %s",
            (user_id, image_id),
        )
        count: int = cur.fetchone()[0]
        return count + 1


def save_attempt(
    conn,
    user_id: str,
    image_id: str,
    prompt_id: str,
    similarity_score: float,
) -> str:
    """Insert an attempt row and return its new UUID."""
    attempt_number = _get_attempt_number(conn, user_id, image_id)
    with conn.cursor() as cur:
        new_id = str(uuid.uuid4())
        cur.execute(
            """
            INSERT INTO attempts
                (id, user_id, image_id, prompt_id, similarity_score,
                 time_taken, attempt_number, created_at)
            VALUES (%s, %s, %s, %s, %s, 0, %s, NOW())
            RETURNING id
            """,
            (new_id, user_id, image_id, prompt_id, similarity_score, attempt_number),
        )
        return str(cur.fetchone()[0])
