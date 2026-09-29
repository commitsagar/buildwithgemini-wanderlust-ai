# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

try:
    from app.a2ui.basic_catalog.provider import BasicCatalog
    from app.a2ui.schema.manager import A2uiSchemaManager
except ImportError:
    from a2ui.basic_catalog.provider import BasicCatalog
    from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from .a2ui_utils import a2ui_callback



MODEL = "gemini-3.6-flash"


def get_live_weather(city: str) -> str:
    """Fetches real-time live weather conditions for a destination using Open-Meteo's free public API.

    Args:
        city: The name of the city (e.g. Paris, Tokyo, New York, Rome, London).

    Returns:
        Real-time temperature and weather conditions.
    """
    import urllib.parse
    import urllib.request
    import json

    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        req = urllib.request.Request(geo_url, headers={"User-Agent": "WanderlustAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            geo_data = json.loads(response.read().decode())

        if not geo_data.get("results"):
            return f"Could not find coordinates for city: {city}."

        result = geo_data["results"][0]
        lat, lon = result["latitude"], result["longitude"]
        city_name = result.get("name", city)
        country = result.get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        req = urllib.request.Request(weather_url, headers={"User-Agent": "WanderlustAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            weather_data = json.loads(response.read().decode())

        current = weather_data.get("current_weather", {})
        temp_c = current.get("temperature")
        wind = current.get("windspeed")
        temp_f = round((temp_c * 9 / 5) + 32, 1) if temp_c is not None else None

        return (
            f"Live weather for {city_name}, {country}: "
            f"{temp_c}°C ({temp_f}°F), wind speed: {wind} km/h (Source: Open-Meteo API)."
        )
    except Exception as e:
        return f"Error fetching live weather for {city}: {str(e)}"


def convert_currency(amount: float, from_currency: str = "USD", to_currency: str = "EUR") -> str:
    """Converts money between world currencies using live exchange rates from the free Frankfurter API.

    Args:
        amount: Amount of money to convert.
        from_currency: 3-letter currency code (e.g. USD, EUR, GBP, JPY, CAD).
        to_currency: 3-letter target currency code (e.g. EUR, JPY, GBP, USD).

    Returns:
        Converted amount and live exchange rate.
    """
    import urllib.request
    import json

    from_curr = from_currency.upper().strip()
    to_curr = to_currency.upper().strip()

    try:
        url = f"https://api.frankfurter.dev/v1/latest?amount={amount}&base={from_curr}&symbols={to_curr}"
        req = urllib.request.Request(url, headers={"User-Agent": "WanderlustAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())

        converted = data.get("rates", {}).get(to_curr)
        date = data.get("date", "today")
        if converted is not None:
            rate = round(converted / amount, 4) if amount != 0 else 0
            return f"{amount} {from_curr} = {converted} {to_curr} (Rate: 1 {from_curr} = {rate} {to_curr}, Date: {date})."
        return f"Unable to convert from {from_curr} to {to_curr}."
    except Exception as e:
        return f"Error fetching live exchange rates: {str(e)}"


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def search_dietary_restaurants(city: str, dietary_tag: str = "any", cuisine: str = "any") -> str:
    """Finds dining spots tailored to dietary restrictions (e.g., vegan, gluten-free, halal, vegetarian).

    Args:
        city: City or destination to search in (e.g., Paris, Tokyo, New York, San Francisco).
        dietary_tag: Dietary restriction or preference (e.g., gluten-free, vegan, vegetarian, halal, celiac).
        cuisine: Optional cuisine preference (e.g., French, Japanese, Italian, Bakery).

    Returns:
        A list of matching restaurant recommendations.
    """
    city_lower = city.lower()
    tag_lower = dietary_tag.lower()

    database = {
        "paris": [
            {"name": "Noglu", "cuisine": "French Bakery & Bistro", "dietary": ["gluten-free", "celiac-safe"], "neighborhood": "7th Arr.", "rating": 4.9, "highlight": "100% celiac-certified brioche, gourmet quiches, and fruit tarts."},
            {"name": "Le Potager du Marais", "cuisine": "Traditional French", "dietary": ["vegan", "vegetarian"], "neighborhood": "Le Marais", "rating": 4.8, "highlight": "Plant-based French classics including vegan onion soup and bourguignon."},
            {"name": "Wild & The Moon", "cuisine": "Healthy Cafe", "dietary": ["gluten-free", "vegan", "dairy-free"], "neighborhood": "Saint-Honoré", "rating": 4.6, "highlight": "Superfood bowls, cold-pressed elixirs, and raw gluten-free desserts."}
        ],
        "tokyo": [
            {"name": "Gluten Free T's Kitchen", "cuisine": "Japanese Classics", "dietary": ["gluten-free", "celiac-safe", "vegan"], "neighborhood": "Roppongi", "rating": 4.9, "highlight": "Gluten-free gyoza, ramen, and tempura made with domestic rice flour."},
            {"name": "Ain Soph. Journey", "cuisine": "Plant-based Comfort", "dietary": ["vegan", "vegetarian"], "neighborhood": "Shinjuku", "rating": 4.7, "highlight": "Famous fluffy vegan heavenly pancakes, matcha parfaits, and bento sets."},
            {"name": "Brown Rice by Neal's Yard", "cuisine": "Organic Washoku", "dietary": ["vegan", "vegetarian", "organic"], "neighborhood": "Omotesando", "rating": 4.8, "highlight": "Seasonal steamed baskets and fermented miso sets in a quiet garden."}
        ],
        "new york": [
            {"name": "Senza Gluten", "cuisine": "Italian Trattoria", "dietary": ["gluten-free", "celiac-safe"], "neighborhood": "Greenwich Village", "rating": 4.8, "highlight": "100% dedicated gluten-free handmade pasta, garlic bread, and tiramisu."},
            {"name": "Dirt Candy", "cuisine": "Creative Vegetable Gastronomy", "dietary": ["vegetarian", "vegan"], "neighborhood": "Lower East Side", "rating": 4.9, "highlight": "Michelin-starred vegetable-centric tasting menus."},
            {"name": "Planta Queen", "cuisine": "Asian Fusion", "dietary": ["vegan", "halal-friendly", "gluten-free"], "neighborhood": "Nomad", "rating": 4.8, "highlight": "Delectable plant-based sushi nigiri, dumplings, and spicy Dan Dan noodles."}
        ]
    }

    restaurants = database.get(city_lower, [
        {"name": f"The Green Table ({city.title()})", "cuisine": cuisine if cuisine != "any" else "Local Bistro", "dietary": [dietary_tag if dietary_tag != "any" else "vegetarian options"], "neighborhood": "Downtown", "rating": 4.7, "highlight": "Farm-to-table seasonal kitchen catering to all dietary requirements."}
    ])

    if tag_lower != "any":
        filtered = [r for r in restaurants if any(tag_lower in d for d in r["dietary"])]
        if filtered:
            restaurants = filtered

    lines = [f"Recommended dining in {city.title()} for '{dietary_tag}':"]
    for r in restaurants:
        lines.append(f"- **{r['name']}** ({r['cuisine']}, {r['neighborhood']}) - Rating: {r['rating']}★ | Diets: {', '.join(r['dietary'])} | Note: {r['highlight']}")
    return "\n".join(lines)


# Hardcoded project ID required for Firestore client to work properly across local and Agent Platform
PROJECT_ID = "qwiklabs-gcp-03-5d6b9bcda8e5"


def get_travel_bookmarks(city: str = "", category: str = "") -> str:
    """Reads saved travel bookmarks from the Firestore collection.

    Args:
        city: Optional city filter (e.g. Paris, San Francisco).
        category: Optional category filter (e.g. Restaurant, Cafe, Event).

    Returns:
        A list of matching bookmarks saved in the database.
    """
    from google.cloud import firestore

    db = firestore.Client(project=PROJECT_ID)
    docs = db.collection("travel_bookmarks").stream()
    items = []
    for doc in docs:
        data = doc.to_dict()
        if city and city.lower() not in data.get("city", "").lower():
            continue
        if category and category.lower() not in data.get("category", "").lower():
            continue
        items.append(data)

    if not items:
        return f"No travel bookmarks found for city='{city}' category='{category}'."

    lines = ["Saved Travel Bookmarks:"]
    for item in items:
        diets = f" | Diets: {', '.join(item.get('dietary_tags', []))}" if item.get("dietary_tags") else ""
        lines.append(
            f"- **{item.get('name')}** [{item.get('category')}] in {item.get('city')} ({item.get('neighborhood')}) "
            f"- Rating: {item.get('rating')}★{diets} | Notes: {item.get('notes')}"
        )
    return "\n".join(lines)


def save_travel_bookmark(
    name: str,
    city: str,
    category: str = "Restaurant",
    neighborhood: str = "Central",
    dietary_tags: str = "",
    notes: str = "",
) -> str:
    """Saves a new recommendation or favorite spot into the Firestore travel_bookmarks collection.

    Args:
        name: Name of the spot or event (e.g. 'Le Potager du Marais', 'Louvre Museum').
        city: Destination city (e.g. 'Paris', 'Tokyo').
        category: Category such as Restaurant, Cafe, Attraction, or Event.
        neighborhood: Area or arrondissement.
        dietary_tags: Comma-separated dietary tags if applicable (e.g. 'gluten-free, vegan').
        notes: Helpful notes or highlights.

    Returns:
        Confirmation of the saved bookmark.
    """
    from google.cloud import firestore
    import re

    db = firestore.Client(project=PROJECT_ID)
    doc_id = re.sub(r"[^a-zA-Z0-9_-]", "-", f"{name.lower()}-{city.lower()}").strip("-")
    tags = [t.strip() for t in dietary_tags.split(",") if t.strip()] if dietary_tags else []

    data = {
        "id": doc_id,
        "name": name,
        "city": city.title(),
        "category": category.title(),
        "neighborhood": neighborhood,
        "dietary_tags": tags,
        "notes": notes,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    db.collection("travel_bookmarks").document(doc_id).set(data)
    return f"Successfully saved bookmark '{name}' in {city.title()} to Firestore!"


def geocode_address(address: str) -> str:
    """Uses Google Maps Geocoding API to turn an address or landmark into geographic coordinates (latitude, longitude).

    Args:
        address: The address or place to geocode (e.g., 'Eiffel Tower, Paris' or '1600 Amphitheatre Pkwy, Mountain View, CA').

    Returns:
        Formatted address and latitude/longitude coordinates.
    """
    import os
    import urllib.parse
    import urllib.request
    import json

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key or api_key == "PASTE_KEY_HERE":
        return "Error: GOOGLE_MAPS_API_KEY environment variable is not configured. Please set a valid key in .env."

    try:
        encoded = urllib.parse.quote(address)
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded}&key={api_key}"
        req = urllib.request.Request(url, headers={"User-Agent": "WanderlustAI/1.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())

        status = data.get("status")
        if status != "OK":
            err_msg = data.get("error_message", "")
            return f"Geocoding API returned status '{status}': {err_msg}"

        results = data.get("results", [])
        if not results:
            return f"No geocoding results found for address: '{address}'."

        first = results[0]
        formatted = first.get("formatted_address")
        location = first.get("geometry", {}).get("location", {})
        lat = location.get("lat")
        lng = location.get("lng")
        place_id = first.get("place_id")

        return f"Geocoded '{address}':\n- Formatted Address: {formatted}\n- Coordinates: Latitude {lat}, Longitude {lng}\n- Place ID: {place_id}"
    except Exception as e:
        return f"Error contacting Google Maps Geocoding API: {str(e)}"


def search_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "restaurant",
    radius_meters: float = 1000.0,
    max_results: int = 5,
) -> str:
    """Uses Google Places API (New) to search for nearby places around coordinates.

    Args:
        latitude: Latitude of the center point.
        longitude: Longitude of the center point.
        place_type: Place type to include (e.g. restaurant, cafe, tourist_attraction, museum, bakery).
        radius_meters: Radius in meters to search within (default 1000m).
        max_results: Maximum number of results to return (1-20, default 5).

    Returns:
        Key fields for matching places: display name, formatted address, and location coordinates.
    """
    import os
    import urllib.request
    import json

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key or api_key == "PASTE_KEY_HERE":
        return "Error: GOOGLE_MAPS_API_KEY environment variable is not configured. Please set a valid key in .env."

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types,places.rating",
    }

    body = {
        "includedTypes": [place_type.lower().strip()],
        "maxResultCount": min(max(1, max_results), 20),
        "locationRestriction": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": float(radius_meters),
            }
        },
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())

        places = data.get("places", [])
        if not places:
            return f"No nearby places found of type '{place_type}' within {radius_meters}m of ({latitude}, {longitude})."

        lines = [f"Found {len(places)} nearby '{place_type}' places:"]
        for p in places:
            name = p.get("displayName", {}).get("text", "Unknown")
            address = p.get("formattedAddress", "No address")
            loc = p.get("location", {})
            lat = loc.get("latitude")
            lng = loc.get("longitude")
            rating = p.get("rating", "N/A")
            lines.append(f"- **{name}** (Rating: {rating}★)\n  Address: {address}\n  Coordinates: ({lat}, {lng})")

        return "\n".join(lines)
    except Exception as e:
        return f"Error contacting Google Places API (New): {str(e)}"


# Hardcoded Cloud Storage bucket for Wanderlust AI visual assets
STORAGE_BUCKET_NAME = "wanderlust-ai-qwiklabs-gcp-03-5d6b9bcda8e5"


async def generate_destination_image(
    prompt: str,
    tool_context: "ToolContext",
) -> str:
    """Generates an image for a travel destination, scenic postcard, restaurant dish, or festival.

    Uses gemini-3.1-flash-lite-image in the global region.
    Saves the image artifact to the Playground Artifacts panel and uploads it to the public Cloud Storage bucket.

    Args:
        prompt: Detailed description of the image to generate (e.g. 'Scenic vintage postcard of the Eiffel Tower in Paris at sunset').
        tool_context: ADK ToolContext used to save session artifacts.

    Returns:
        The public HTTPS URL of the image hosted in Cloud Storage.
    """
    import uuid
    import re
    from google import genai
    from google.genai import types
    from google.cloud import storage

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        image_bytes = None
        mime_type = "image/jpeg"

        for part in response.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/jpeg"
                break

        if not image_bytes:
            return "Error: No image was returned by gemini-3.1-flash-lite-image."

        # 1. Save with tool_context.save_artifact so it shows in Playground's Artifacts panel
        ext = "png" if "png" in mime_type else "jpg"
        clean_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", prompt[:30]).strip("_").lower()
        filename = f"{clean_slug}_{uuid.uuid4().hex[:6]}.{ext}"

        artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # 2. Upload the same image bytes to the public Cloud Storage bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(STORAGE_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{filename}"
        return f"Image generated successfully!\n- Public URL: {public_url}\n- Artifact saved: {filename}"
    except Exception as e:
        return f"Error generating destination image: {str(e)}"


async def generate_destination_video(
    prompt: str,
    tool_context: "ToolContext",
) -> str:
    """Generates a short, realistic video preview for a travel destination, landmark, activity, or food scene.

    Uses Google's Omni video model (gemini-omni-flash-preview) in the global region.
    Saves the video artifact with tool_context.save_artifact so it shows in the Playground Artifacts panel,
    and uploads the video bytes to the public Cloud Storage bucket, returning its public HTTPS URL.

    Args:
        prompt: Detailed description of the video clip to generate (e.g. 'Cinematic aerial video of Mount Fuji at sunrise with rolling mist').
        tool_context: ADK ToolContext used to save session artifacts.

    Returns:
        The public HTTPS URL of the video hosted in Cloud Storage.
    """
    import uuid
    import re
    import base64
    import asyncio
    import google.auth
    import google.auth.transport.requests
    import requests
    from google.genai import types
    from google.cloud import storage

    creds, project = google.auth.default()
    creds.refresh(google.auth.transport.requests.Request())

    url = f"https://aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/global/interactions"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    body = {
        "model": "gemini-omni-flash-preview",
        "background": True,
        "input": [{"type": "text", "text": prompt}],
        "response_format": [
            {
                "type": "video",
                "aspect_ratio": "16:9",
                "duration": "3s",
            }
        ],
        "generation_config": {
            "video_config": {
                "task": "text_to_video",
            }
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code != 200:
            return f"Error initiating video generation with Omni: {resp.text}"

        data = resp.json()
        interaction_id = data.get("id")
        if not interaction_id:
            return f"Error: No interaction ID returned from Omni: {data}"

        poll_url = f"{url}/{interaction_id}"
        video_bytes = None
        mime_type = "video/mp4"

        # Poll for completion (up to ~90s)
        for _ in range(18):
            await asyncio.sleep(5)
            poll_resp = requests.get(poll_url, headers=headers, timeout=20)
            if poll_resp.status_code != 200:
                continue
            poll_data = poll_resp.json()
            status = poll_data.get("status")
            if status == "completed":
                for step in poll_data.get("steps", []):
                    if step.get("type") == "model_output":
                        for content in step.get("content", []):
                            if content.get("type") == "video":
                                b64 = content.get("data")
                                if b64:
                                    video_bytes = base64.b64decode(b64)
                                    mime_type = content.get("mime_type", "video/mp4")
                                    break
                break
            elif status == "failed":
                return f"Error: Omni video generation failed: {poll_data.get('error')}"

        if not video_bytes:
            return "Error: Timed out waiting for Omni video generation to complete."

        # 1. Save artifact with tool_context.save_artifact for Playground Artifacts panel
        clean_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", prompt[:30]).strip("_").lower()
        filename = f"{clean_slug}_{uuid.uuid4().hex[:6]}.mp4"
        artifact_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
        await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # 2. Upload video bytes to public Cloud Storage bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(STORAGE_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{STORAGE_BUCKET_NAME}/{filename}"
        return f"Video preview generated successfully with Omni!\n- Public Video URL: {public_url}\n- Artifact saved: {filename}"
    except Exception as e:
        return f"Error generating destination video with Omni: {str(e)}"


from google.adk.code_executors import AgentEngineSandboxCodeExecutor

# Agent Engine Reasoning Engine resource name from deployment_metadata.json
AGENT_ENGINE_RESOURCE_NAME = "projects/57498790528/locations/us-east1/reasoningEngines/6688775633482285056"
SANDBOX_RESOURCE_NAME = "projects/57498790528/locations/us-east1/reasoningEngines/6688775633482285056/sandboxEnvironments/7997346203140358144"

sandbox_code_executor = AgentEngineSandboxCodeExecutor(
    sandbox_resource_name=SANDBOX_RESOURCE_NAME,
    agent_engine_resource_name=AGENT_ENGINE_RESOURCE_NAME,
)

async def generate_memories_callback(callback_context: CallbackContext):
    """After each turn, send the session to Vertex AI Memory Bank for extraction."""
    await callback_context.add_session_to_memory()
    return None


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are Wanderlust AI, an expert travel concierge. "
        "You remember the user's stated travel preferences, dietary restrictions, and ALWAYS remember all user allergies "
        "(e.g., peanuts, shellfish, dairy, gluten, celiac disease, tree nuts) from previous conversations and strictly respect them when suggesting food or activities. "
        "Help travelers discover destinations, find dietary-tailored restaurants, "
        "check live weather, convert currencies with real exchange rates, "
        "lookup geographic coordinates with Google Geocoding, find nearby spots with Google Places, "
        "generate visual postcards and destination images with Gemini Image, "
        "generate short video previews with Google Omni (gemini-omni-flash-preview), "
        "run Python computations and budget calculations using your code execution sandbox, "
        "and read/write their saved travel bookmarks using Firestore."
    ),
    workflow_description="Analyze the request, call tools to gather accurate data, and return structured UI when appropriate.",
    ui_description=(
        "If responding with UI, keep every surface tiny, flat, and compact: ONE Card > ONE Column > components. "
        "Total maximum 5 components across the whole surface. "
        "Never nest Cards inside Cards or create deep component trees. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "When generating or showing an image, include an Image component in the Column child list alongside title/description Text, "
        "and set its URL to the public https link returned by generate_destination_image, for example: "
        '{"id": "img1", "component": {"Image": {"url": {"literalString": "https://storage.googleapis.com/..."}}}}. '
        "Never point an Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    code_executor=sandbox_code_executor,
    tools=[
        PreloadMemoryTool(),
        generate_destination_image,
        generate_destination_video,
        search_dietary_restaurants,
        geocode_address,
        search_nearby_places,
        get_live_weather,
        convert_currency,
        get_travel_bookmarks,
        save_travel_bookmark,
        get_current_time,
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
