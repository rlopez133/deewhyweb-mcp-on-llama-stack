Spin up an instance of https://catalog.demo.redhat.com/catalog?utm_source=webapp&utm_medium=share-link&search=rhel+ai&item=babylon-catalog-prod%2Frhdp.rhel-ai-vm.prod  select a g6.12xlarge instance

ilab config init

Select Nividia -> 4xL0S

Grab your hf token from hugging face

`ilab model download -rp ibm-granite/granite-3.1-8b-instruct --hf-token <token>`

`ilab model serve --model-path  /var/home/instruct/.cache/instructlab/models/ibm-granite/granite-3.1-8b-instruct/ --gpus 4 -- --served-model-name llama31-8b`

From another terminalm setup an SSH tunnel listening on port 8001

`ssh -L 8001:localhost:8000 instruct@bastion.xxxx.sandboxxxx.opentlc.com`

Run llama stack with podman:

`podman run -it -p 5051:5051 -v ./run.yaml:/tmp/run.yaml:Z llamastack/distribution-remote-vllm --yaml-config /tmp/run.yaml --port 5051 --env INFERENCE_MODEL=llama31-8b --env VLLM_URL=http://host.containers.internal:8001/v1`

Run npm install
`npm install`

Run the node.js app with supergateway

`npx -y supergateway --stdio "node index.js"`

Create the mcp toolgroup 

```
curl -X POST -H "Content-Type: application/json" \
--data \
'{ "provider_id" : "model-context-protocol", "toolgroup_id" : "builtin::weather", "mcp_endpoint" : { "uri" : "http://host.containers.internal:8000/sse"}}' \
 localhost:5051/v1/toolgroups 
 ```

Test the mcp connection, you should see getforcast as the identier, and the parameters populated correctly.

`llama-stack-client toolgroups get builtin::weather `
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


Test with python


`python -m mcp localhost 5051`

Error:  
`400: Invalid value: 'getforecast' is not a valid BuiltinTool`
