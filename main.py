import os
import json
from typing import Annotated, List
from openai import OpenAI
from contextlib import asynccontextmanager
import debugpy
from fastapi import Body, FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from settings import get_settings

settings = get_settings()
openai = OpenAI(api_key=settings.OPEN_AI_KEY)
origins = ["*"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "60000"
    debugpy.listen(("0.0.0.0", 4000))
    print("Debug Listener Started on 4000...")
    yield
    debugpy.stop()


app = FastAPI(
    title="OpenAI API Backend",
    description="API Backend to test integration with OpenAPI",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(
    prompt: Annotated[str, Body(description="The prompt to send to the OpenAI API")],
    files: Annotated[
        List[UploadFile],
        File(
            description="JSON Files to send to the OpenAI API",
            media_type="application/json",
            # button text
            title="Upload JSON Files",
        ),
    ],
):
    # Validate files to be JSON
    for file in files:
        if file.content_type != "application/json":
            raise HTTPException(status_code=400, detail="Invalid File Type")

    # Read and parse JSON files
    json_contents = []
    for file in files:
        content = await file.read()
        try:
            json_content = json.loads(content)
            json_contents.append(json_content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON File")

    # Combine all JSON contents into a single list of data
    combined_data = []
    for content in json_contents:
        combined_data.extend(content if isinstance(content, list) else [content])

    # Construct messages for OpenAI
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides insights based on search result data.",
        },
        {
            "role": "user",
            "content": f"Here is the search result data: {json.dumps(combined_data)}",
        },
        {"role": "user", "content": f"{prompt}"},
    ]

    # Make the API call to OpenAI
    response = openai.chat.completions.create(model="gpt-4", messages=messages)

    return response.choices[0].message.content
