# MCP on LLAMA-STACK

# Pre-reqs

* podman or docker
* llama-stack-client  (pip install llama-stack-client)
* [Ollama](https://ollama.com/)

Instructions for configuring llama-stack to integrate with a locally running MCP server and Ollama

## Run llama3.2:3b-instruct with Ollama 

`ollama run llama3.2:3b-instruct-fp16 --keepalive 60m`

## Build llama-stack for Ollama provider

Clone the llama-stack repository

`git clone https://github.com/meta-llama/llama-stack.git`

`cd llama-stack`

`pip install .`

`llama stack build --template ollama`

You may need to install and configure conda first, for more information checkout the docs: https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html

## Run llama-stack

`export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"`

`export LLAMA_STACK_PORT=8321`

`llama stack run  ../run-ollama.yaml`

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

Test the mcp connection, you should see getforcast as the identier, and the parameters populated correctly.

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


`python -m mcp localhost 8321`

You should get a response similar to:

```
No available shields. Disabling safety.
Using model: meta-llama/Llama-3.2-3B-Instruct
inference> [getforecast(latitude=42.4217, longitude=-71.0931)]
tool_execution> Tool:getforecast Args:{'latitude': 42.4217, 'longitude': -71.0931}
tool_execution> Tool:getforecast Response:{"type":"text","text":"Forecast for 42.4217, -71.0931:\n\nThis Afternoon:\nTemperature: 33°F\nWind: 9 mph SW\nMostly Cloudy\n---\nTonight:\nTemperature: 18°F\nWind: 2 to 6 mph W\nMostly Cloudy\n---\nWednesday:\nTemperature: 33°F\nWind: 5 to 9 mph NE\nSlight Chance Snow Showers\n---\nWednesday Night:\nTemperature: 27°F\nWind: 6 to 10 mph E\nLight Snow\n---\nThursday:\nTemperature: 45°F\nWind: 7 to 12 mph SW\nRain And Snow\n---\nThursday Night:\nTemperature: 21°F\nWind: 8 to 13 mph W\nSlight Chance Light Rain then Partly Cloudy\n---\nFriday:\nTemperature: 30°F\nWind: 10 to 14 mph W\nSunny\n---\nFriday Night:\nTemperature: 16°F\nWind: 3 to 8 mph W\nPartly Cloudy\n---\nSaturday:\nTemperature: 36°F\nWind: 2 to 7 mph SW\nMostly Cloudy then Chance Light Snow\n---\nSaturday Night:\nTemperature: 30°F\nWind: 7 mph SE\nSnow Likely then Rain And Snow\n---\nSunday:\nTemperature: 41°F\nWind: 7 to 12 mph S\nRain And Snow\n---\nSunday Night:\nTemperature: 20°F\nWind: 12 mph NW\nRain And Snow Likely\n---\nWashington's Birthday:\nTemperature: 27°F\nWind: 15 mph W\nSlight Chance Light Snow then Mostly Sunny\n---\nMonday Night:\nTemperature: 10°F\nWind: 13 mph W\nPartly Cloudy\n---"}
inference> The weather forecast for Portsmouth, NH is:

* Today: Partly Cloudy, Temperature: 33°F, Wind: 9 mph SW
* Tonight: Mostly Cloudy, Temperature: 18°F, Wind: 2 to 6 mph W
* Tomorrow (Wednesday): Slight Chance Snow Showers, Temperature: 33°F, Wind: 5 to 9 mph NE
* Tomorrow Night (Wednesday Night): Light Snow, Temperature: 27°F, Wind: 6 to 10 mph E
* Thursday: Rain and Snow, Temperature: 45°F, Wind: 7 to 12 mph SW
* Thursday Night (Thursday Night): Slight Chance Light Rain then Partly Cloudy, Temperature: 21°F, Wind: 8 to 13 mph W
* Friday: Sunny, Temperature: 30°F, Wind: 10 to 14 mph W
* Friday Night (Friday Night): Partly Cloudy, Temperature: 16°F, Wind: 3 to 8 mph W
* Saturday: Mostly Cloudy then Chance Light Snow, Temperature: 36°F, Wind: 2 to 7 mph SW
* Saturday Night (Saturday Night): Snow Likely then Rain and Snow, Temperature: 30°F, Wind: 7 mph SE
* Sunday: Rain and Snow, Temperature: 41°F, Wind: 7 to 12 mph S
* Sunday Night (Sunday Night): Rain and Snow Likely, Temperature: 20°F, Wind: 12 mph NW
* Washington's Birthday: Slight Chance Light Snow then Mostly Sunny, Temperature: 27°F, Wind: 15 mph W
* Monday Night (Monday Night): Partly Cloudy, Temperature: 10°F, Wind: 13 mph W
```