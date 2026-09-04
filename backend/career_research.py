from featherless_client import client, MODEL


def research_career(role):

    prompt = f"""
You are the Career Research Agent for SkillGap Navigator.

The student wants to become:
{role}

Analyze the skills and knowledge normally required for this role.

Return ONLY valid JSON in this format:

{{
    "role": "{role}",
    "required_skills": [],
    "preferred_skills": [],
    "tools_and_technologies": [],
    "important_concepts": [],
    "typical_entry_level_expectations": []
}}

Rules:
- Keep the skills specific.
- Separate required skills from preferred skills.
- Include technologies and tools separately.
- Focus on entry-level and undergraduate candidates.
- Do not add explanations outside the JSON.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a structured career research agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    role = input("Enter target career role: ")

    result = research_career(role)

    print("\n========== CAREER RESEARCH ==========\n")
    print(result)
    print("\n======================================\n")