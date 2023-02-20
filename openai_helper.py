#!/usr/bin/python3
import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")
print(f"KEY got {openai.api_key}")

def ask_bot(text: str, max_tokens: int=16, temperature:float = 1.0)-> str:
  completion = openai.Completion.create(
    model="text-davinci-003",
    prompt=text,
    max_tokens=max_tokens,
    temperature=temperature
  )
  return completion.choices[0].text

def gen_img(text: str, size: str="512x512", num: int=1): 
  img_urls = []
  image_response = openai.Image.create(
    prompt=text,
    n=num,
    size=size
  )
  for u in image_response.data:
    img_urls.append(u.url)
  return img_urls
    
if __name__ == "__main__":
  print(gen_img("A girl with long golden hair"))