from app.constants import ROUND_CHANNEL

CHANNEL = ROUND_CHANNEL

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
        "target_prompt": (
            "Weathered stone temple ruins covered in vines, jungle setting, dramatic shafts of "
            "sunlight, moss-covered statues, cinematic lighting, photorealistic."
        ),
    },
    {
        "id": "futuristic-city",
        "title": "Futuristic City",
        "difficulty": "hard",
        "reference_image": "futuristic-city.jpg",
        "target_prompt": (
            "Sprawling cyberpunk metropolis at night, towering glass skyscrapers with neon "
            "billboards, flying vehicles between buildings, rain-slicked streets reflecting "
            "purple and teal lights, ultra-detailed, cinematic."
        ),
    },
    {
        "id": "golden-sunset",
        "title": "Golden Sunset",
        "difficulty": "easy",
        "reference_image": "golden-sunset.jpeg",
        "target_prompt": (
            "Warm golden-hour sunset over a calm ocean horizon, soft orange and pink sky, "
            "silhouetted clouds, gentle reflections on the water, photographic."
        ),
    },
    {
        "id": "snowy-forest",
        "title": "Snowy Forest",
        "difficulty": "easy",
        "reference_image": "snowy-forest.jpg",
        "target_prompt": (
            "Quiet evergreen forest blanketed in fresh snow, tall pine trees, soft overcast "
            "light, footprints in the snow, serene winter atmosphere, photographic."
        ),
    },
    {
        "id": "underwater-world",
        "title": "Underwater World",
        "difficulty": "medium",
        "reference_image": "underwater-world.jpeg",
        "target_prompt": (
            "Vibrant coral reef teeming with tropical fish, clear blue water with sunbeams "
            "filtering down from the surface, sea turtle in the foreground, photorealistic "
            "underwater photography."
        ),
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
GET_ROUND_HISTORY_FEATURE = "get_round_history"
