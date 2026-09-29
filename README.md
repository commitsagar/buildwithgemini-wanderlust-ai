# Wanderlust AI ✈️🌍

An agentic travel concierge and dietary itinerary planner built with Google Agent Development Kit (ADK) and Gemini on Google Cloud Platform. Wanderlust AI helps travelers explore global destinations, discover dietary-safe dining (vegan, gluten-free, allergy-conscious), generate scenic vintage postcards and cinematic Omni video previews, plan interactive daily schedules with calendar exports, and compute travel budgets.

[![Wanderlust AI Live Demo](https://storage.googleapis.com/wanderlust-ai-qwiklabs-gcp-03-5d6b9bcda8e5/demo.gif)](https://wanderlust-frontend-57498790528.us-east1.run.app)

> 🌐 **Live Portal**: [wanderlust-frontend-57498790528.us-east1.run.app](https://wanderlust-frontend-57498790528.us-east1.run.app)  
> 🎥 **Direct Video Preview**: [Watch High-Definition Demo MP4](https://storage.googleapis.com/wanderlust-ai-qwiklabs-gcp-03-5d6b9bcda8e5/demo.mp4) (with Gemini World Tour frame)

---

## 🌟 What Wanderlust AI Does

Wanderlust AI is built as a multi-tool reasoning agent that coordinates specialized services across Google Cloud:

1. **Travel Portal & Interactive Concierge Drawer**:
   - Modern travel landing page with destination cards (Tokyo, Paris, Mount Fuji, London) and culinary themes (vegan spots, celiac bakeries, outdoor hikes).
   - Embedded floating AI travel concierge drawer with instant suggestions and live chat.

2. **Cinematic Omni Video Previews (`gemini-omni-flash-preview`)**:
   - Generates realistic, physics-grounded destination video clips using Google's Omni model.
   - Automatically saves session artifacts to the ADK panel, uploads to Cloud Storage, and renders in an inline HTML5 video player.

3. **Scenic Visual Postcards (Cloud Storage & Gemini Flash Lite)**:
   - Uses `gemini-3.1-flash-lite-image` to generate custom destination imagery, saves session artifacts, and hosts public visual assets in Cloud Storage.

4. **Multi-Day Timeline & Calendar Synchronization (`.ICS` Export)**:
   - Automatically parses multi-day itineraries into visual day-by-day timeline cards.
   - Generates `.ics` calendar files on the fly for one-click import into Apple Calendar / Outlook, and provides direct Google Calendar sync links.

5. **Dietary-Conscious Dining & Allergen Safety**:
   - Dedicated dining queries respecting strict allergies (nuts, shellfish, gluten, dairy) and dietary choices (100% plant-based, halal, kosher).

6. **Interactive A2UI Card Responses**:
   - Delivers structured responses using the open A2UI protocol (v0.8) for clean visual summaries with embedded images and layout components.

7. **Agent Engine Sandbox Code Execution**:
   - Performs budget estimations, split calculations, and multi-currency conversions inside a secure Google Cloud Agent Engine Sandbox environment.

8. **Cross-Session Long-Term Memory**:
   - Connected to Vertex AI Agent Platform Memory Bank via `PreloadMemoryTool` and automated memory extraction callbacks to remember dietary preferences, favorite cuisines, and previous trips across sessions.

9. **Live Data Grounding**:
   - Fetches live weather conditions, local timezones, and address geocoordinates via real-time web grounding and Google Maps APIs.

10. **Trip Bookmarks Persistence (Firestore)**:
    - Saves favorite restaurants, attractions, and hotels directly into a Google Cloud Firestore collection (`travel_bookmarks`).

---

## 🏗️ Architecture & Google Cloud Stack

- **Agent Framework**: Google Agent Development Kit (ADK) with Gemini 2.5 Flash (`gemini-2.5-flash`).
- **Omni Video Model**: Google Omni (`gemini-omni-flash-preview`) in the `global` region.
- **Image Generation**: Gemini Flash Lite Image (`gemini-3.1-flash-lite-image`).
- **Agent Protocol**: Agent-to-Agent (A2A) protocol powered by `a2a-sdk`.
- **UI Engine**: A2UI (v0.8 Basic Catalog) with custom lightweight HTML5/JS renderer.
- **Agent Platform Memory Bank**: Managed long-term memory via Vertex AI Agent Engine.
- **Code Execution**: Managed isolated code execution in Agent Engine Sandbox.
- **Database**: Google Cloud Firestore (Native mode collection `travel_bookmarks`).
- **Asset Storage**: Google Cloud Storage public asset bucket.
- **Hosting**: Google Cloud Run serverless deployment (`wanderlust-frontend`).

---

## 🚀 Local Development & Setup

### Prerequisites

- Python 3.11+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Google Cloud SDK (`gcloud`) authenticated to your GCP project:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  gcloud config set project YOUR_PROJECT_ID
  ```

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/commitsagar/buildwithgemini-wanderlust-ai.git
cd buildwithgemini-wanderlust-ai

# Set up virtual environment and install dependencies
uv sync
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
PROJECT_ID=YOUR_PROJECT_ID
LOCATION=us-east1
STORAGE_BUCKET_NAME=YOUR_PUBLIC_GCS_BUCKET
GOOGLE_MAPS_API_KEY=YOUR_OPTIONAL_MAPS_KEY
```

### 3. Run the Agent Locally

To launch the local ADK Web playground:

```bash
uv run adk web . --port 8080 --allow_origins "*" --reload_agents
```

### 4. Run the Travel Portal Frontend

To launch the standalone FastAPI travel portal UI:

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

Then visit your local browser at `http://localhost:8080`.

---

## 📹 Demo Assets

The repository contains:
- `demo.gif`: Lightweight animated preview for GitHub and web embedding.
- `demo.mp4`: Universal H.264 video with fast-start playback.
- `demo.webm`: High-resolution VP9 master recording with the Gemini World Tour frame.

