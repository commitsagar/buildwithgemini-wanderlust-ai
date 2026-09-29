# Wanderlust AI ✈️🌍

An agentic travel concierge and dietary itinerary planner built with Google Agent Development Kit (ADK) and Gemini on Google Cloud Platform. Wanderlust AI helps travelers research destinations, discover dietary-safe dining (vegan, gluten-free, allergy-conscious), generate scenic vintage postcards, plan daily schedules, and compute travel budgets.

![Wanderlust AI Demo](demo.gif)

---

## 🌟 What Wanderlust AI Does

Wanderlust AI is built as a reasoning agent that coordinates specialized tools and services to deliver contextual travel assistance:

1. **Dietary-Conscious Dining & Destination Knowledge**:
   - Researches food spots, allergens, and dietary accommodations (vegan, celiac/gluten-free, nut allergies) across global destinations.
2. **Scenic Visual Postcards (Cloud Storage & Gemini Flash Lite)**:
   - Uses `gemini-3.1-flash-lite-image` to generate custom destination imagery, saves session artifacts, and uploads the images to a Google Cloud Storage bucket for direct visual display.
3. **Interactive A2UI Card Responses**:
   - Delivers structured responses using the open A2UI protocol (v0.8) for clean visual summaries with embedded images and layout components.
4. **Agent Engine Sandbox Code Execution**:
   - Performs budget estimations, split calculations, and multi-currency conversions inside a secure Google Cloud Agent Engine Sandbox environment.
5. **Cross-Session Long-Term Memory**:
   - Connected to Vertex AI Agent Platform Memory Bank via `PreloadMemoryTool` and automated memory extraction callbacks to remember dietary preferences, favorite cuisines, and previous trips across sessions.
6. **Live Data Grounding**:
   - Fetches live weather conditions, local timezones, and address geocoordinates via real-time web grounding and public APIs.
7. **Trip Bookmarks Persistence (Firestore)**:
   - Saves favorite restaurants, attractions, and hotels directly into a Google Cloud Firestore collection (`travel_bookmarks`).

---

## 🏗️ Architecture & Google Cloud Stack

- **Agent Framework**: Google Agent Development Kit (ADK) with Gemini 2.5 Flash (`gemini-2.5-flash`).
- **Agent Protocol**: Agent-to-Agent (A2A) protocol powered by `a2a-sdk`.
- **UI Engine**: A2UI (v0.8 Basic Catalog) with custom lightweight HTML5/JS renderer.
- **Agent Platform Memory Bank**: Managed long-term memory via Vertex AI Agent Engine.
- **Code Execution**: Managed isolated code execution in Agent Engine Sandbox.
- **Image Generation & Storage**: `gemini-3.1-flash-lite-image` + Google Cloud Storage.
- **Database**: Google Cloud Firestore (Datastore mode / Native collection).
- **Frontend / Proxy**: FastAPI server serving an emerald-themed web UI with suggestion chips, communicating over A2A.

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

### 4. Run the Custom Frontend

To launch the standalone FastAPI chat UI with suggestion chips:

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

Then visit your local browser at `http://localhost:8080`.

---

## 📹 Demo Video

The repository includes `demo.webm` (high-quality recording with the Gemini World Tour frame) and `demo.gif` for inline GitHub viewing.
