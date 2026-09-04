import requests
import json
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path


URL = "https://vit.ac.in/campus-category/teams"

OUTPUT_FILE = str(Path(__file__).resolve().parent / "data" / "vit_teams.json")


print("\n==============================================")
print("         VIT TEAMS DATA COLLECTOR")
print("==============================================")


def normalize(text):
    return " ".join(text.split()).strip()


# ==================================================
# DOWNLOAD PAGE
# ==================================================

print("\nFetching VIT Teams page...")

response = requests.get(
    URL,
    timeout=20,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

print("✓ Teams page downloaded")


soup = BeautifulSoup(
    response.text,
    "html.parser"
)


# ==================================================
# KNOWN VIT TEAM CATEGORIES
# ==================================================

TEAM_NAMES = [
    "SAE-Teams",
    "ASCE",
    "SEDS",
    "ASME",
    "Team-VAUV",
    "Projects-Lab",
    "RoboVITics",
    "SME Team"
]


# ==================================================
# EXTRACT TEXT BLOCKS
# ==================================================

main_content = soup.find("main")

if main_content is None:
    main_content = soup


elements = main_content.find_all(
    [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "p"
    ]
)


blocks = []

for element in elements:

    text = normalize(
        element.get_text(" ", strip=True)
    )

    if text:
        blocks.append(
            (
                element.name,
                text
            )
        )


# ==================================================
# COLLECT TEAMS
# ==================================================

teams = []


for index, (tag, name) in enumerate(blocks):

    # Only consider headings as possible team names
    if tag not in [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5"
    ]:
        continue


    matched_name = None


    for team_name in TEAM_NAMES:

        if (
            name.lower()
            == team_name.lower()
        ):

            matched_name = team_name
            break


    if matched_name is None:
        continue


    # ------------------------------------------------
    # Collect description until next heading
    # ------------------------------------------------

    description_parts = []


    for next_tag, next_text in blocks[index + 1:]:

        if next_tag in [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5"
        ]:
            break


        if len(next_text) < 20:
            continue


        description_parts.append(
            next_text
        )


        if len(
            " ".join(description_parts)
        ) > 3000:

            break


    description = normalize(
        " ".join(description_parts)
    )


    teams.append({

        "name": matched_name,

        "type": "team",

        "category": "Student Team",

        "school": "",

        "eligible_programmes": [],

        "year_constraints": [],

        "skills": [],

        "career_domains": [],

        "description": description,

        "source_url": URL,

        "last_verified": str(date.today())

    })


# ==================================================
# REMOVE DUPLICATES
# ==================================================

unique_teams = {}


for team in teams:

    key = team["name"].lower()

    if key not in unique_teams:

        unique_teams[key] = team


teams = list(
    unique_teams.values()
)


# ==================================================
# SAVE DATA
# ==================================================

data = {

    "source":
        "VIT Official Student Teams",

    "institution":
        "VIT Vellore",

    "last_verified":
        str(date.today()),

    "teams":
        teams

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


# ==================================================
# DISPLAY RESULT
# ==================================================

print("\n==============================================")

print(
    f"✓ Saved {len(teams)} team entries"
)

print(
    f"✓ File: {OUTPUT_FILE}"
)

print("==============================================")


print("\nTeams collected:\n")


for number, team in enumerate(
    teams,
    start=1
):

    print(
        f"{number:02d}. "
        f"{team['name']}"
    )


print("\n==============================================")