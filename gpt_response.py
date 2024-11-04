import openai

def get_gpt_solution(issue):
    openai.api_key = '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'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Diagnose and provide a solution for: {issue}",
        max_tokens=50
    )
    return response.choices[0].text.strip()
