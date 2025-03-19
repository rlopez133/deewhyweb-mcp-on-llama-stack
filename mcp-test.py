# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
import os
import fire
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from termcolor import colored

def main(host: str, port: int):
    client = LlamaStackClient(
        base_url=f"http://{host}:{port}",
    )
    available_shields = [shield.identifier for shield in client.shields.list()]
    if not available_shields:
        print(colored("No available shields. Disabling safety.", "yellow"))
    else:
        print(f"Available shields found: {available_shields}")
    available_models = [
        model.identifier for model in client.models.list() if model.model_type == "llm"
    ]
    if not available_models:
        print(colored("No available models. Exiting.", "red"))
        return
    else:
        selected_model = available_models[0]
        print(f"Using model: {selected_model}")
    agent_config = AgentConfig(
        model=selected_model,
        instructions="You are a helpful assistant. When asked about weather, use the getforecast tool with latitude and longitude parameters.",
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
        },
        toolgroups=(
            [
                "mcp::weather"
            ]
        ),
        tool_choice="auto",
        input_shields=available_shields if available_shields else [],
        output_shields=available_shields if available_shields else [],
        enable_session_persistence=False,
    )
    agent = Agent(client, agent_config)
    user_prompts = [
        "Based on the weather this week in New York, what's the best day to walk around the city?",
    ]
    session_id = agent.create_session("test-session")
    for prompt in user_prompts:
        print(f"\nUser: {prompt}")
        response = agent.create_turn(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            session_id=session_id,
        )

        # Fix: process the response chunks directly
        inference_text = ""
        for chunk in response:
            if hasattr(chunk, 'event') and hasattr(chunk.event, 'payload'):
                payload = chunk.event.payload

                # Look for step_progress events with text chunks
                if hasattr(payload, 'event_type') and payload.event_type == 'step_progress':
                    if hasattr(payload, 'delta') and hasattr(payload.delta, 'text'):
                        print(payload.delta.text, end="", flush=True)

                # Or look for the final complete message
                elif hasattr(payload, 'event_type') and payload.event_type == 'turn_complete':
                    if hasattr(payload, 'turn') and hasattr(payload.turn, 'output_message'):
                        inference_text = payload.turn.output_message.content

        # Print the final complete message if found
        if inference_text:
            print(f"\n\ninference> {inference_text}")

if __name__ == "__main__":
    fire.Fire(main)
