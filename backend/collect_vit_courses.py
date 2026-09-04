import requests
import json
from bs4 import BeautifulSoup
from datetime import date


URL = "https://vit.ac.in/schools/school-of-computer-science-and-engineering-for-ug-courses"

OUTPUT_FILE = "data/vit_courses.json"


print("\n==============================================")
print("        VIT COURSE DATA COLLECTOR")
print("==============================================")


# ==================================================
# DOWNLOAD PAGE
# ==================================================

print("\nFetching VIT CSE UG curriculum page...")

response = requests.get(
    URL,
    timeout=20,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response.raise_for_status()

print("✓ Course page downloaded")


soup = BeautifulSoup(
    response.text,
    "html.parser"
)


# ==================================================
# COURSE KEYWORDS
# ==================================================

course_keywords = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analytics",
    "Natural Language Processing",
    "Image Processing",
    "Computer Vision",
    "Cloud Computing",
    "Distributed Computing",
    "Parallel Computing",
    "Open Source Programming",
    "Cyber Security",
    "Computer Networks",
    "Database",
    "Big Data",
    "Software Engineering",
    "Algorithms",
    "Data Structures",
    "Python",
    "Statistics",
    "Linear Algebra",
    "Optimization",
    "Blockchain",
    "Internet of Things",
    "IoT",
    "Robotics"
]


# ==================================================
# EXTRACT TABLE DATA
# ==================================================

courses = []


tables = soup.find_all("table")

print(
    f"✓ Found {len(tables)} curriculum tables"
)


for table in tables:

    rows = table.find_all("tr")

    for row in rows:

        cells = row.find_all(
            ["td", "th"]
        )

        if not cells:
            continue

        row_text = [
            " ".join(
                cell.get_text(
                    " ",
                    strip=True
                ).split()
            )
            for cell in cells
        ]

        combined = " | ".join(row_text)


        # ------------------------------------------
        # Check whether row contains useful course
        # ------------------------------------------

        matched_keyword = None

        for keyword in course_keywords:

            if keyword.lower() in combined.lower():

                matched_keyword = keyword
                break


        if matched_keyword is None:
            continue


        # ------------------------------------------
        # Store row
        # ------------------------------------------

        course_name = row_text[0]

        if len(course_name) < 3:
            continue


        courses.append({

            "name": course_name,

            "type": "course",

            "school": "School of Computer Science and Engineering",

            "programme": "B.Tech CSE",

            "category": matched_keyword,

            "skills": [],

            "career_domains": [],

            "description": combined,

            "source_url": URL,

            "last_verified": str(date.today())

        })


# ==================================================
# REMOVE DUPLICATES
# ==================================================

unique_courses = {}


for course in courses:

    key = (
        course["name"].lower()
        + "|"
        + course["programme"].lower()
    )

    if key not in unique_courses:

        unique_courses[key] = course


courses = list(
    unique_courses.values()
)


# ==================================================
# SAVE
# ==================================================

data = {

    "source":
        "VIT Official Academic Information",

    "institution":
        "VIT Vellore",

    "last_verified":
        str(date.today()),

    "courses":
        courses

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
# RESULT
# ==================================================

print("\n==============================================")

print(
    f"✓ Saved {len(courses)} course entries"
)

print(
    f"✓ File: {OUTPUT_FILE}"
)

print("==============================================")


print("\nCourses detected:\n")


for number, course in enumerate(
    courses,
    start=1
):

    print(
        f"{number:02d}. "
        f"{course['name']}"
    )


print("\n==============================================")