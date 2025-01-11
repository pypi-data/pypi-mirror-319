# openai_tools_decorator

A lightweight Python library that streamlines creating and invoking “tools” (functions) in your OpenAI ChatCompletion-based projects. It lets you register and call both **synchronous** and **asynchronous** functions via decorators.

## Installation

```bash
pip install openai_tools_decorator
```

## Quick Start

### 1. Import and Initialization

```python
from openai_tools_decorator import OpenAIT

client = OpenAIT()
```

### 2. Adding Tools

```python
@client.add_tool(
    {
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name in English"}
            },
            "required": ["city"]
        },
    }
)
def get_weather(city: str):
    return f"Weather in {city}: 25°C"
```

### 3. Using Tools with Chat

```python
user_input = "How cold is it in Moscow right now?"
response = await client.run_with_tool(
    user_input,
    messages=[],
    model="gpt-4o"
)
print(response)  # The assistant’s response, possibly including a tool call
```

### 4. Removing Tools

To remove a tool, use `remove_tool` with function's name as an argument:

```python
client.remove_tool("get_weather")
```

If the tool is not found, `remove_tool` will raise `ValueError`.

## Example

```python
import asyncio
import aiohttp
from openai_tools_decorator import OpenAIT

client = OpenAIT()
api_key = "<YOUR_API_KEY>"

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

@client.add_tool(
    {
        "description": "Fetch weather from an API",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name in English"
                }
            },
            "required": ["city"]
        },
    }
)
async def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    return await fetch_url(url)

async def main():
    question = "What's the temperature in London?"
    result = await client.run_with_tool(question, messages=[])
    print("Assistant says:", result)

asyncio.run(main())
```

## Key Points

-   You can register **sync and async ** functions.
-   Tools are automatically registered and described for the OpenAI model.
-   The model decides whether to call a tool during the dialogue.
-   You can quickly remove unnecessary tools using `remove_tool`.

## License

Distributed under MIT or any other license of your choice. Contributions and feedback are always welcome!
