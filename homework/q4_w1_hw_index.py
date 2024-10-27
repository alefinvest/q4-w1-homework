import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Enhanced function to generate the appropriate prompt based on the user's input.
def handle_input(option, user_input):
    prompts = {
        "2": f"Suggest a detailed recipe for {user_input}",  # Ingredient-based
        "1": f"Suggest a detailed recipe for {user_input}",  # Dish name request
        "3": f"I need your feedback on the recipe. Suggest improvements to the following recipe {user_input}: ..."  # Recipe critique
    }
    return prompts.get(option, "I can help with ingredient-based suggestions, recipe requests, or critiques. What would you like to do?")

# Set the first message
messages = [
  {
    "role": "system",
    "content": "You are an Spanish experienced chef specializing in vegetarian \
                cuisine. You are willing to help people by suggesting \
                detailed vegetarian recipes for dishes they want to cook. \
                If someone asks you about dishes or ingredients related to \
                meat or fish, politely tell them that you only handle \
                inquiries about vegetarian cuisine.",
  }
]

# Add another system instruction
messages.append(
  {
    "role": "system",
    "content": "The client will ask you one of these three topics: \
                ingredient-based dish suggestions, recipe requests for \
                specific dishes or recipe critiques and improvement \
                suggestions. If you don't know the dish or the \
                ingredient, you should answer that you don't know the \
                dish or ingredient and end the conversation.",
  }
)

# More instructions
messages.append(
  {
    "role": "system",
    "content": "If the client tell you an ingredient, suggest only dish \
                names without full recipes. If you are asked for dish \
                name then provide a detailed recipe. If the client tells \
                you a recipe, offer suggested improvements.",
  }
)

# Specify the model used
model = "gpt-4o-mini"

# Menu
while True:
  print("1. I want the recipe for an specific dish")
  print("2. I want a recipe for an specific ingredients")
  print("3. I want suggestions to improve a recipe that I know")
  option = input("Choose an option (1-3): ")

  if option in ["1", "2", "3"]:
    break
  else:
    print("Invalid option. Please choose 1, 2, or 3.")

# Make the prompt
if option == "1":
  dish = input("Enter the name of the dish you want the recipe for: ")
elif option == "2":
  ingredients = input("Enter the name of the ingredient you want a recipe for: ")
else:
  recipe = input("Enter the recipe you want to improve: ")

# Generate the prompt using the handle_input function
prompt = handle_input(option, dish if option == "1" else ingredients if option == "2" else recipe)
print(prompt)

# Add the user message
messages.append(
  {
    "role": "user",
    "content": prompt,
  }
)

# Make the API call
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")