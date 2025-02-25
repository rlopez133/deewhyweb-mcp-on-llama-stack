# MCP on LLAMA-STACK

# Pre-reqs
* node.js (tested with v20.17.0)
* llama-stack-client  (pip install llama-stack-client)

Instructions for configuring llama-stack to integrate with a locally running MCP server and vllm

## Run llama3.2:3b-instruct with vllm on a RHEL instance 

`curl -o tool_chat_template_llama3.2_json.jinja https://raw.githubusercontent.com/vllm-project/vllm/refs/heads/main/examples/tool_chat_template_llama3.2_json.jinja`

Serve the meta-llama/Llama-3.2-8B-Instruct model

`vllm serve  meta-llama/Llama-3.2-3B-Instruct --gpu_memory_utilization 1  --tensor-parallel-size 2 --pipeline-parallel-size 2  --enable-auto-tool-choice --tool-call-parser llama3_json --chat-template ./tool_chat_template_llama3.2_json.jinja `

## Connect via ssh tunnel

`ssh -L 8001:localhost:8000 instruct@bastion.xxxx.sandboxxxx.opentlc.com`

## Build llama-stack for Ollama provider

Clone the llama-stack repository

`git clone https://github.com/meta-llama/llama-stack.git`

Currently tested with the `test-agents-web-vllm` branch from `https://github.com/bbrowning/llama-stack.git`

`cd llama-stack`

`pip install .`

`llama stack build --template remote-vllm`

You may need to install and configure conda first, for more information checkout the docs: https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html

## Run llama-stack

`export VLLM_URL=http://localhost:8001/v1      `

`export INFERENCE_MODEL=meta-llama/Llama-3.2-3B-Instruct  `

`llama stack run  ./run-vllm.yaml`

## Deploy the node.js mcp server app

Run npm install

`npm install`

Run the node.js app with supergateway

`npx -y supergateway --stdio "node app/index.js"`


## Create the mcp toolgroup 

```
curl -X POST -H "Content-Type: application/json" \
--data \
'{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::weather", "mcp_endpoint" : { "uri" : "http://localhost:8000/sse"}}' \
 localhost:8321/v1/toolgroups 
 ```

Test the mcp connection, you should see getforecast as the identier, and the parameters populated correctly.

`llama-stack-client toolgroups get mcp::weather `
```
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ description           ┃ identifier  ┃ metadata              ┃ parameters            ┃ provider_id           ┃ provider_resource_id ┃ tool_host             ┃ toolgroup_id     ┃ type ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ Get weather forecast  │ getforecast │ {'endpoint':          │ [Parameter(descripti… │ model-context-protoc… │ getforecast          │ model_context_protoc… │ builtin::weather │ tool │
│ for a location        │             │ 'http://host.contain… │ of the location',     │                       │                      │                       │                  │      │
│                       │             │                       │ name='latitude',      │                       │                      │                       │                  │      │
│                       │             │                       │ parameter_type='numb… │                       │                      │                       │                  │      │
│                       │             │                       │ required=True,        │                       │                      │                       │                  │      │
│                       │             │                       │ default=None),        │                       │                      │                       │                  │      │
│                       │             │                       │ Parameter(descriptio… │                       │                      │                       │                  │      │
│                       │             │                       │ of the location',     │                       │                      │                       │                  │      │
│                       │             │                       │ name='longitude',     │                       │                      │                       │                  │      │
│                       │             │                       │ parameter_type='numb… │                       │                      │                       │                  │      │
│                       │             │                       │ required=True,        │                       │                      │                       │                  │      │
│                       │             │                       │ default=None)]        │                       │                      │                       │                  │      │
└───────────────────────┴─────────────┴───────────────────────┴───────────────────────┴───────────────────────┴──────────────────────┴───────────────────────┴──────────────────┴──────┘
```


## Test with python


`python -m mcp-test localhost 8321`

You should get a response similar to:

```
No available shields. Disabling safety.
Using model: meta-llama/Llama-3.2-3B-Instruct
inference> 
tool_execution> Tool:getforecast Args:{'latitude': '40.7128', 'longitude': '-74.0060'}
tool_execution> Tool:getforecast Response:{"type":"text","text":"Forecast for 40.7128, -74.0060:\n\nThis Afternoon:\nTemperature: 56°F\nWind: 8 mph S\nChance Rain Showers\n---\nTonight:\nTemperature: 39°F\nWind: 8 mph W\nSlight Chance Rain Showers then Partly Cloudy\n---\nWednesday:\nTemperature: 53°F\nWind: 7 to 10 mph W\nSunny\n---\nWednesday Night:\nTemperature: 42°F\nWind: 7 mph S\nMostly Cloudy then Slight Chance Rain Showers\n---\nThursday:\nTemperature: 56°F\nWind: 9 to 13 mph SW\nChance Rain Showers\n---\nThursday Night:\nTemperature: 40°F\nWind: 13 mph W\nChance Rain Showers\n---\nFriday:\nTemperature: 46°F\nWind: 13 to 18 mph NW\nSunny\n---\nFriday Night:\nTemperature: 35°F\nWind: 8 to 14 mph SW\nMostly Cloudy\n---\nSaturday:\nTemperature: 53°F\nWind: 10 to 14 mph SW\nSlight Chance Rain And Snow Showers\n---\nSaturday Night:\nTemperature: 29°F\nWind: 14 mph NW\nSlight Chance Rain Showers\n---\nSunday:\nTemperature: 36°F\nWind: 16 mph NW\nSunny\n---\nSunday Night:\nTemperature: 24°F\nWind: 13 to 16 mph NW\nMostly Clear\n---\nMonday:\nTemperature: 39°F\nWind: 13 mph NW\nSunny\n---\nMonday Night:\nTemperature: 31°F\nWind: 6 to 9 mph W\nPartly Cloudy\n---","annotations":null}
inference> Based on the weather forecast for New York, the best day to walk around the city would be Wednesday. It is expected to be sunny with a temperature of 53°F and a wind speed of 7 to 10 mph.
```