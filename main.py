import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from openai.types.responses.container_network_policy_allowlist_param import Iterable

_ = load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("No api key was found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

parser = argparse.ArgumentParser(description="Simple Chatbot using OpenRouter and OpenAI")
_ = parser.add_argument("user_prompt", type=str, help="User prompt being sent to the free openrouter api.")
_ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output of the command.")
args = parser.parse_args()

messages = [
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages= messages
)

if response.usage == None:
    raise RuntimeError("Possibly failed API call.  No token usage data from the chat completion response.")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

print(f"Response:\n{response.choices[0].message.content}")
