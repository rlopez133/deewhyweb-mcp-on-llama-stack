import os
import sys
import asyncio
import fire
import subprocess


from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.client_tool import client_tool

pre_path = "/home/thoraxe/bin/"


@client_tool
async def get_object_namespace_list(kind: str, namespace: str) -> str:
    """Get the list of all objects in a namespace

    :param kind: the type of object
    :param namespace: the name of the namespace
    :returns: a plaintext list of the kind object in the namespace
    """
    output = subprocess.run(
        [pre_path + "oc", "get", kind, "-n", namespace, "-o", "name"],
        capture_output=True,
        timeout=2,
    )
    return output.stdout


async def run_main(host: str, port: int, user_query: str, disable_safety: bool = False):
    client = LlamaStackClient(
        base_url=f"http://{host}:{port}",
    )

    #client_tools = {
    #    "tool_name": "get_object_namespace_list",
    #    "description": "Get the list of all objects in a namespace",
    #    "parameters": {
    #        "kind": {
    #            "param_type": "string",
    #            "description": "the type of object"
    #        },
    #        "namespace": {
    #             "param_type": "string",
    #             "description": "the name of the namespace"
    #        }
    #    },
    #    "required": [
    #        "kind",
    #        "namespace"
    #    ]
    #}
    client_tools = {
        "tool_name": "get_weather",
        "description": "Get the current weather",
        "parameters": {
            "location": {
                "param_type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
        },
    }
    def extract_tool_invocation_content(response):
        tool_invocation_content: str = ""
        for chunk in response:
            delta = chunk.event.delta
            print(delta)
            if delta.type == "tool_call" and delta.parse_status == "succeeded":
                call = delta.tool_call
                tool_invocation_content += f"[{call.tool_name}, {call.arguments}]"
        return tool_invocation_content

    response = client.inference.chat_completion(
        model_id="meta-llama/Llama-3.2-3B-Instruct",
        messages=[
            {"role": "system", "content": '''You are a helpful assistant with access to the following
function calls. Your task is to produce a list of function calls
necessary to generate response to the user utterance. Use the following
function calls as required.'''},
            {"role": "user", "content": user_query},
        ],
        tools=[
            client_tools
        ],
        stream=True
    )
    print(extract_tool_invocation_content(response))

def main(host: str, port: int, user_query: str):
    asyncio.run(run_main(host, port, user_query))


if __name__ == "__main__":
    fire.Fire(main)