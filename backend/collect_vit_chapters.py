import requests
import json
from bs4 import BeautifulSoup
from datetime import date


SOURCES = {
    "Indian Societies":
        "https://vit.ac.in/campus/chapters/indiansocieties",

    "International Societies":
        "https://vit.ac.in/campus/chapters/international-societies",

    "IEEE Chapters":
        "https://vit.ac.in/campus/chapters/ieeechapters"
}


CHAPTER_NAMES = {

    "Indian Societies": [
        "SESI",
        "ISHRAE",
        "IGS",
        "AMSI",
        "ADI",
        "CSI",
        "ISGF",
        "IICHE",
        "ISET",
        "ISTE",
        "IWRS",
        "IE(I)",
        "BRSI",
        "ISOI",
        "VITMAS",
        "ICI",
        "NASA"
    ],

    "International Societies": [
        "AICHE",
        "ASME",
        "Objective- IxDA",
        "ASCE-VIT",
        "SAE-VIT",
        "Ashrae",
        "ACM",
        "AEE",
        "IDSA",
        "IETE",
        "IISE",
        "IMECHE",
        "ISA",
        "ASM",
        "Oikos",
        "OSA",
        "SBE",
        "SIAM",
        "SME",
        "SPE",
        "SEDS",
        "IET",
        "Sigma Xi",
        "TMI"
    ],

    "IEEE Chapters": [
        "IEEE-PELS",
        "IEEE-ITS",
        "IEEE",
        "IEEE - COMSOC",
        "IEEE- CAS",
        "IEEE - CS",
        "IEEE - EDS",
        "IEEE-EMBS",
        "IEEE - IAS",
        "IEEE - MTTS",
        "IEEE-NPSS",
        "IEEE - PES",
        "IEEE-PSES",
        "IEEE-PCS",
        "IEEE-RAS",
        "IEEE - SPS",
        "IEEE-SSIT",
        "IEEE-TEMS",
        "IEEE-WIE"
    ]
}


OUTPUT_FILE = "data/vit_chapters.json"


print("\n==============================================")
print("       VIT CHAPTER DATA COLLECTOR")
print("==============================================")


def normalize(text):
    return " ".join(text.split()).strip()


def collect_category(category, url):

    print(f"\nFetching {category}...")

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print(f"✓ {category} page downloaded")

    # Get all visible text blocks
    blocks = []

    for element in soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "p", "div"]
    ):

        text = normalize(element.get_text(" ", strip=True))

        if text:
            blocks.append(text)

    chapters = []

    names = CHAPTER_NAMES[category]

    for i, chapter_name in enumerate(names):

        # Find the first block containing the chapter name
        start_index = None

        for index, block in enumerate(blocks):

            if block.lower() == chapter_name.lower():
                start_index = index
                break

        if start_index is None:

            # Try partial matching
            for index, block in enumerate(blocks):

                if chapter_name.lower() in block.lower():
                    start_index = index
                    break

        if start_index is None:
            print(f"⚠ Could not locate: {chapter_name}")
            continue

        # Collect text after the chapter name
        description_parts = []

        for block in blocks[start_index + 1:]:

            # Stop when another known chapter starts
            is_next_chapter = False

            for other_name in names:

                if block.lower() == other_name.lower():
                    is_next_chapter = True
                    break

            if is_next_chapter:
                break

            # Ignore navigation / duplicate short blocks
            if len(block) < 30:
                continue

            description_parts.append(block)

            # Prevent enormous descriptions
            if len(" ".join(description_parts)) > 2500:
                break

        description = normalize(
            " ".join(description_parts)
        )

        chapters.append({

            "name": chapter_name,

            "type": "chapter",

            "category": category,

            "school": "",

            "eligible_programmes": [],

            "year_constraints": [],

            "skills": [],

            "career_domains": [],

            "description": description,

            "source_url": url,

            "last_verified": str(date.today())

        })

        print(f"✓ {chapter_name}")

    return chapters


# ==================================================
# COLLECT ALL CATEGORIES
# ==================================================

all_chapters = []


for category, url in SOURCES.items():

    try:

        category_chapters = collect_category(
            category,
            url
        )

        all_chapters.extend(category_chapters)

        print(
            f"\n✓ {category}: "
            f"{len(category_chapters)} chapters"
        )

    except Exception as error:

        print(
            f"⚠ Error collecting "
            f"{category}: {error}"
        )


# ==================================================
# REMOVE DUPLICATES
# ==================================================

unique_chapters = {}

for chapter in all_chapters:

    key = (
        chapter["category"].lower()
        + "|"
        + chapter["name"].lower()
    )

    unique_chapters[key] = chapter


all_chapters = list(
    unique_chapters.values()
)


# ==================================================
# SAVE JSON
# ==================================================

data = {

    "source":
        "VIT Official Student Chapters",

    "institution":
        "VIT Vellore",

    "last_verified":
        str(date.today()),

    "categories": [
        "Indian Societies",
        "International Societies",
        "IEEE Chapters"
    ],

    "chapters":
        all_chapters
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
# FINAL OUTPUT
# ==================================================

print("\n==============================================")
print(
    f"✓ Saved {len(all_chapters)} chapter entries"
)
print(
    f"✓ File: {OUTPUT_FILE}"
)
print("==============================================")

print("\nChapter entries:\n")

for number, chapter in enumerate(
    all_chapters,
    start=1
):

    print(
        f"{number:02d}. "
        f"[{chapter['category']}] "
        f"{chapter['name']}"
    )

print("\n==============================================")