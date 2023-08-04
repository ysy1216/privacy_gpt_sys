#cloud3 gpt3.5
import openai

def cloud_model3(content):
  openai.api_key = "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"
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",  # gpt-3.5-turbo-0301、text-davinci-003
    messages=[
      {"role": "user", "content": content}
    ],
    temperature=0.5,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.5,
  )

  return response.choices[0].message.content
