FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "python3 -m vllm.entrypoints.openai.api_server --model ibm-granite/granite-guardian-3.1-2b --port 5000 & python3 models/guardian_filter.py"]
