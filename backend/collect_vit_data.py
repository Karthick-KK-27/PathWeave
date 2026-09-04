import requests
import json
from bs4 import BeautifulSoup

URL = "https://vit.ac.in/campus/clubs/technical"
OUTPUT_FILE = "data/vit_clubs.json"

print("\n==============================================")
print("       VIT CLUB DATA COLLECTOR")
print("==============================================")
print("\nFetching official VIT technical club page...")

response = requests.get(
    URL,
    timeout=20,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

print("✓ VIT page downloaded")

soup = BeautifulSoup(response.text, "html.parser")


# ------------------------------------------------
# CLUB NAMES FROM THE OFFICIAL VIT PAGE
# ------------------------------------------------

club_names = [
    "ALPHA BIO CELL (ABC)",
    "Apple Developers Group",
    "ARCHI-TECH",
    "BULLS AND BEARS",
    "VIT BLOCKCHAIN COMMUNITY",
    "ADMARK",
    "MULTIMEDIA CLUB",
    "DIGIT SQUAD",
    "THE AI & ML CLUB",
    "ASTRONOMY CLUB",
    "LINUX USER'S GROUP",
    "DEVELOPERS STUDENT CLUB",
    "CSED",
    "CODECHEF",
    "CREATION LAB",
    "DREAM MERCHANTS",
    "E2PC",
    "E-CELL",
    "INNOVATOR'S QUEST",
    "IOTHINC",
    "MOZILLA FIREFOX",
    "ROBOVITICS",
    "SOLAI CLUB",
    "SABEST",
    "TAG",
    "THE CATALYST CLUB",
    "TEC",
    "VISUAL BLOGGER'S",
    "VIT AMATEUR RADIO CLUB (VARC)"
]


# ------------------------------------------------
# GET ALL TEXT FROM PAGE
# ------------------------------------------------

main_content = soup.find("main")

if main_content is None:
    main_content = soup

elements = main_content.find_all(
    ["h1", "h2", "h3", "h4", "h5", "p"]
)


# ------------------------------------------------
# EXTRACT EACH CLUB + ITS OWN DESCRIPTION
# ------------------------------------------------

clubs = []

for index, club_name in enumerate(club_names):

    description_parts = []

    # Find the heading/text corresponding to this club
    start_index = None

    for i, element in enumerate(elements):

        text = element.get_text(" ", strip=True)

        if text.lower() == club_name.lower():

            start_index = i
            break

    if start_index is None:

        print(f"⚠ Could not locate: {club_name}")

        clubs.append({
            "name": club_name,
            "category": "Technical Club",
            "description": "",
            "skills": [],
            "career_relevance": [],
            "eligibility": "VIT students",
            "source_url": URL
        })

        continue


    # Collect text until the next club heading
    for element in elements[start_index + 1:]:

        text = element.get_text(" ", strip=True)

        if not text:
            continue

        # Stop when another known club begins
        is_next_club = any(
            text.lower() == other.lower()
            for other in club_names
            if other.lower() != club_name.lower()
        )

        if is_next_club:
            break

        # Avoid navigation / irrelevant headings
        if text in ["Technical", "Students' Welfare", "Student Clubs"]:
            continue

        description_parts.append(text)


    description = " ".join(description_parts).strip()


    clubs.append({
        "name": club_name,
        "category": "Technical Club",
        "description": description,
        "skills": [],
        "career_relevance": [],
        "eligibility": "VIT students",
        "source_url": URL
    })


# ------------------------------------------------
# REMOVE DUPLICATES
# ------------------------------------------------

unique_clubs = {}

for club in clubs:

    key = club["name"].lower()

    if key not in unique_clubs:
        unique_clubs[key] = club


clubs = list(unique_clubs.values())


# ------------------------------------------------
# SAVE JSON
# ------------------------------------------------

data = {
    "source": "VIT Official Technical Clubs",
    "institution": "VIT Vellore",
    "source_url": URL,
    "last_verified": "2026-09-04",
    "clubs": clubs
}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        indent=4,
        ensure_ascii=False
    )


# ------------------------------------------------
# RESULT
# ------------------------------------------------

print("\n==============================================")
print(f"✓ Saved {len(clubs)} clubs")
print(f"✓ File: {OUTPUT_FILE}")
print("==============================================")

print("\nClub names collected:\n")

for number, club in enumerate(clubs, start=1):

    print(
        f"{number:02d}. {club['name']}"
    )

print("\n==============================================")