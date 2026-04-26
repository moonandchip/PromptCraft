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
    # EASY
    {
        "id": "golden-sunset",
        "title": "Golden Sunset",
        "difficulty": "easy",
        "reference_image": "golden-sunset.jpeg",
        "target_prompt": "Warm golden-hour sunset over a calm ocean horizon, soft orange and pink sky, gentle reflections on the water, minimal elements, photorealistic",
    },
    {
        "id": "snowy-forest",
        "title": "Snowy Forest",
        "difficulty": "easy",
        "reference_image": "snowy-forest.jpg",
        "target_prompt": "Quiet evergreen forest covered in fresh snow, tall pine trees, soft overcast lighting, peaceful winter atmosphere, photorealistic",
    },
    {
        "id": "desert-road",
        "title": "Desert Road",
        "difficulty": "easy",
        "reference_image": "desert-road.jpg",
        "target_prompt": "A long straight road through a desert landscape, clear blue sky, warm sunlight, minimal scenery, photorealistic",
    },
    {
        "id": "mountain-lake",
        "title": "Mountain Lake",
        "difficulty": "easy",
        "reference_image": "mountain-lake.jpg",
        "target_prompt": "A calm mountain lake reflecting snow-capped peaks, clear sky, still water, natural lighting, photorealistic",
    },
    {
        "id": "sandy-beach",
        "title": "Sandy Beach",
        "difficulty": "easy",
        "reference_image": "sandy-beach.jpg",
        "target_prompt": "A quiet sandy beach with gentle ocean waves, clear horizon, soft daylight, minimal elements, photorealistic",
    },
    {
        "id": "green-field",
        "title": "Green Field",
        "difficulty": "easy",
        "reference_image": "green-field.jpg",
        "target_prompt": "A wide open green field under a bright blue sky, soft clouds, natural lighting, simple landscape",
    },
    {
    "id": "red-apple",
    "title": "Red Apple",
    "difficulty": "easy",
    "reference_image": "red-apple.jpg",
    "target_prompt": "A single red apple centered on a plain white background, soft lighting, minimal composition, high detail, photorealistic",
    },

    # MEDIUM
    {
        "id": "ancient-temple",
        "title": "Ancient Temple",
        "difficulty": "medium",
        "reference_image": "ancient-temple.jpg",
        "target_prompt": "Weathered stone temple ruins covered in vines, jungle setting, dramatic sunlight beams, moss-covered statues, cinematic lighting, photorealistic",
    },
    {
        "id": "underwater-world",
        "title": "Underwater World",
        "difficulty": "medium",
        "reference_image": "underwater-world.jpeg",
        "target_prompt": "Vibrant coral reef with tropical fish, clear blue water, sunlight filtering through, sea life in motion, photorealistic underwater scene",
    },
    {
        "id": "snow-cabin",
        "title": "Snow Cabin",
        "difficulty": "medium",
        "reference_image": "snow-cabin.jpg",
        "target_prompt": "A cozy wooden cabin in a snowy forest, warm light glowing from windows, snow-covered trees, evening atmosphere, cinematic lighting",
    },
    {
        "id": "jungle-waterfall",
        "title": "Jungle Waterfall",
        "difficulty": "medium",
        "reference_image": "jungle-waterfall.jpg",
        "target_prompt": "A tropical jungle waterfall cascading into a pool, lush green plants, mist in the air, natural lighting, photorealistic",
    },
    {
        "id": "city-sunset",
        "title": "City Sunset",
        "difficulty": "medium",
        "reference_image": "city-sunset.jpg",
        "target_prompt": "A city street at sunset with warm orange lighting, long shadows, buildings lining the road, cinematic perspective",
    },
    {
        "id": "lighthouse-coast",
        "title": "Lighthouse Coast",
        "difficulty": "medium",
        "reference_image": "lighthouse-coast.jpg",
        "target_prompt": "A lighthouse on a rocky coastline, waves crashing against rocks, cloudy sky, dramatic lighting, coastal landscape",
    },

    # HARD
    {
        "id": "futuristic-city",
        "title": "Futuristic City",
        "difficulty": "hard",
        "reference_image": "futuristic-city.jpg",
        "target_prompt": "A futuristic cyberpunk city at night with neon lights, towering skyscrapers, glowing billboards, rain reflections, cinematic lighting, highly detailed",
    },
    {
        "id": "neon-alley",
        "title": "Neon Alley",
        "difficulty": "hard",
        "reference_image": "neon-alley.jpg",
        "target_prompt": "A narrow alley filled with neon lights, wet pavement reflecting colors, dark atmosphere, cyberpunk style, cinematic composition",
    },
    {
        "id": "castle-cliff",
        "title": "Castle Cliff",
        "difficulty": "hard",
        "reference_image": "castle-cliff.jpg",
        "target_prompt": "A large fantasy castle on a cliff overlooking the ocean, dramatic clouds, epic scale, cinematic lighting",
    },
    {
        "id": "foggy-bridge",
        "title": "Foggy Bridge",
        "difficulty": "hard",
        "reference_image": "foggy-bridge.jpg",
        "target_prompt": "A large bridge disappearing into thick fog, muted colors, atmospheric perspective, moody cinematic lighting",
    },
    {
        "id": "desert-ruins",
        "title": "Desert Ruins",
        "difficulty": "hard",
        "reference_image": "desert-ruins.jpg",
        "target_prompt": "Ancient desert ruins partially buried in sand, dark storm clouds approaching, dramatic lighting, cinematic environment",
    },
    {
        "id": "abandoned-control-room",
        "title": "Abandoned Control Room",
        "difficulty": "hard",
        "reference_image": "abandoned-control-room.jpg",
        "target_prompt": "An abandoned industrial control room filled with old control panels, buttons and screens, dim lighting, dusty surfaces, moody cinematic atmosphere",
    },

    # CHALLENGE
    {
        "id": "night-market",
        "title": "Night Market",
        "difficulty": "hard",
        "reference_image": "night-market.jpg",
        "target_prompt": "A busy night market street filled with food stalls and crowds of people, colorful lanterns and glowing lights, deep perspective, cinematic lighting, highly detailed",
    },
    {
        "id": "glowing-forest",
        "title": "Glowing Forest",
        "difficulty": "hard",
        "reference_image": "glowing-forest.jpg",
        "target_prompt": "A dark forest illuminated by glowing bioluminescent plants and mushrooms, soft blue and purple lighting, magical atmosphere, highly detailed",
    },
    {
        "id": "cyberpunk-rooftop",
        "title": "Cyberpunk Rooftop",
        "difficulty": "hard",
        "reference_image": "cyberpunk-rooftop.jpg",
        "target_prompt": "A futuristic rooftop overlooking a neon cyberpunk city at night, glowing signs, rain-soaked surfaces, deep perspective, cinematic lighting",
    },
]

CHALLENGE_ROUND_IDS = [
    "night-market",
    "glowing-forest",
    "cyberpunk-rooftop",
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
