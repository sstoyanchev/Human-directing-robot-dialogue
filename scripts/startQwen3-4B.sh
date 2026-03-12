#!/usr/bin/bash
# requires environment with vllm installed

suffix=$(date +"%Y-%m-%d")

#maxlen='245312'
maxlen='65536'

port='8891'

echo "nohup vllm serve Qwen/Qwen3-4B-Instruct-2507 --port $port --max-model-len=$maxlen >& ./logs/serve_QwenQwen3-4B-Instruct-2507--port${port}--max-model-len${maxlen}_$suffix.log &"

nohup vllm serve Qwen/Qwen3-4B-Instruct-2507 --port $port --max-model-len=$maxlen >& ./logs/serve_QwenQwen3-4B-Instruct-2507--port${port}--max-model-len${maxlen}_$suffix.log &

