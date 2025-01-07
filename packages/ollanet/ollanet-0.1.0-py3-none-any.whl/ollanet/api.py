from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class Query(BaseModel):
    prompt: str
    model: str = "llama2"

@app.post("/generate")
async def generate_text(query: Query):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model, "prompt": query.prompt},
            stream=True
        )
        response.raise_for_status()
        
        collected_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_obj = json.loads(line.decode('utf-8'))
                    collected_response += json_obj['response']
                    if json_obj.get('done', False):
                        break
                except json.JSONDecodeError:
                    pass
                except KeyError:
                    pass
        return Response(content=collected_response, media_type="text/plain")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")