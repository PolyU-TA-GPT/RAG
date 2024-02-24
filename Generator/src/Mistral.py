import requests
import json
import os
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, say 'Sorry that I cannot retrieve the answer from given context.'

{context}

Question: {question}
Helpful Answer:"""

content = """
CHAI is a student in Hong Kong PolyU\\
CHAI is from China\\
END OF RESULT\\
"""

question = "Who is CAO Yixin?"

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",

  },
  data=json.dumps({
    "model": "mistralai/mistral-7b-instruct:free", # Optional
    "messages": [
      {"role": "user", "content": template.format(context=content, question=question)}
    ]
  })
)

print(response.json())