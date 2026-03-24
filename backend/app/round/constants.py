ROUTER_PREFIX = "/round"
ROUTER_TAG = "round"

LEONARDO_API_V1_BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"
LEONARDO_API_V2_BASE_URL = "https://cloud.leonardo.ai/api/rest/v2"
LEONARDO_GENERATIONS_PATH = "/generations"
LEONARDO_API_KEY_ENV_VAR = "LEONARDO_API_KEY"

# Default generation settings
GENERATION_WIDTH = 1024
GENERATION_HEIGHT = 1024
GENERATION_NUM_IMAGES = 1
# Nano Banana model
GENERATION_MODEL_ID = "gemini-2.5-flash-image"

POLL_INTERVAL_SECONDS = 3.0
POLL_MAX_ATTEMPTS = 20

# Static round definitions
ROUNDS: list[dict] = [
    {
        "id": "ancient-temple",
        "title": "Ancient Temple",
        "difficulty": "medium",
        "reference_image": "ancient-temple.jpg",
    },
    {
        "id": "futuristic-city",
        "title": "Futuristic City",
        "difficulty": "hard",
        "reference_image": "futuristic-city.jpg",
    },
    {
        "id": "golden-sunset",
        "title": "Golden Sunset",
        "difficulty": "easy",
        "reference_image": "golden-sunset.jpeg",
    },
    {
        "id": "snowy-forest",
        "title": "Snowy Forest",
        "difficulty": "easy",
        "reference_image": "snowy-forest.jpg",
    },
    {
        "id": "underwater-world",
        "title": "Underwater World",
        "difficulty": "medium",
        "reference_image": "underwater-world.jpeg",
    },
]

ERR_NO_API_KEY = "Leonardo API key is not configured"
ERR_GENERATION_FAILED = "Image generation failed"
ERR_GENERATION_TIMEOUT = "Image generation timed out"
ERR_ROUND_NOT_FOUND = "Round not found"
ERR_GENERATION_API_ERROR = "Leonardo API error"

# Feature names for structured logging
SUBMIT_ROUND_FEATURE = "submit_round"
START_ROUND_FEATURE = "start_round"
GET_ROUND_ATTEMPTS_FEATURE = "get_round_attempts"
GET_ROUNDS_FEATURE = "get_rounds"
