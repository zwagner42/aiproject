import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages,
            temperature=0,
            tools = available_functions,
        )

        if response.usage == None:
            raise RuntimeError("Possibly failed API call.  No token usage data from the chat completion response.")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)

                if not result_message["content"]:
                    raise Exception(f"Empty content returned from the call to {tool_call.function.name}")
                elif args.verbose:
                    print(f"-> {result_message['content']}")

        else:
            print(f"Response:\n{message.content}")
            return

    print("Maximum number of iterations reached without a final response from the agent.")
    sys.exit(1)


main()
