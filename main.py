import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_files_info import get_files_info


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        if verbose:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
        else:
            print(f" - Calling function: {function_call_part.name}")

        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error: calling function")

        print(f"-> {function_call_result.parts[0].function_response.response}")


def call_function(function_call_part, verbose=False):
    args = function_call_part.args
    function_name = function_call_part.name

    if function_name == "get_file_content":
        function_result = get_file_content("calculator", file_path=args["file_path"])

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="get_file_content",
                    response={"result": function_result},
                )
            ],
        )

    if function_name == "run_python_file":
        function_result = run_python_file("calculator", file_path=args["file_path"])

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="run_python_file",
                    response={"result": function_result},
                )
            ],
        )

    if function_name == "write_file":
        function_result = write_file(
            "calculator", file_path=args["file_path"], content=args["content"]
        )

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="write_file",
                    response={"result": function_result},
                )
            ],
        )

    if function_name == "get_files_info":
        function_result = get_files_info("calculator", directory=args["directory"])

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="get_files_info",
                    response={"result": function_result},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )


if __name__ == "__main__":
    main()
