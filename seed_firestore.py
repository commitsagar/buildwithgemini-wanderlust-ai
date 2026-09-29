import datetime
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-5d6b9bcda8e5"

db = firestore.Client(project=PROJECT_ID)
collection_ref = db.collection("travel_bookmarks")

sample_items = [
    {
        "id": "noglu-paris",
        "city": "Paris",
        "name": "Noglu",
        "category": "Restaurant",
        "cuisine": "French Gourmet Bakery & Bistro",
        "dietary_tags": ["gluten-free", "celiac-safe"],
        "neighborhood": "7th Arrondissement",
        "rating": 4.9,
        "notes": "100% celiac-certified brioche, quiches, and fruit tarts.",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "id": "wild-and-moon-paris",
        "city": "Paris",
        "name": "Wild & The Moon",
        "category": "Cafe",
        "cuisine": "Organic Healthy Cafe",
        "dietary_tags": ["gluten-free", "vegan", "dairy-free"],
        "neighborhood": "Saint-Honoré",
        "rating": 4.6,
        "notes": "Superfood bowls, cold-pressed juices, and raw vegan treats.",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "id": "nuit-blanche-paris",
        "city": "Paris",
        "name": "Nuit Blanche Arts Extravaganza",
        "category": "Event",
        "cuisine": "N/A",
        "dietary_tags": [],
        "neighborhood": "Seine Riverbanks",
        "rating": 4.8,
        "notes": "All-night contemporary art exhibits and nocturnal light installations.",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "id": "shizen-sf",
        "city": "San Francisco",
        "name": "Shizen Vegan Sushi Bar",
        "category": "Restaurant",
        "cuisine": "Japanese Vegan & Izakaya",
        "dietary_tags": ["vegan", "plant-based"],
        "neighborhood": "Mission District",
        "rating": 4.9,
        "notes": "Torched specialty sushi rolls using smoked beets and tapioca pearls.",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
]

for item in sample_items:
    doc_id = item["id"]
    collection_ref.document(doc_id).set(item)
    print(f"Seeded bookmark: {doc_id} -> {item['name']}")

print("Seeding complete.")
