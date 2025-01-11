## OpenAI extensions

### Get Pocket OpenAI Tool Spec

```python
import hyperpocket as pk
from pocket_openai import PocketOpenAI

pocket = PocketOpenAI(tools=[
    *pk.curated_tools.SLACK,  # SLACK = [slack_get_message, slack_post_message, ..]
    *pk.curated_tools.LINEAR,
    "https://github.com/my-org/some-awesome-tool"]
)

# get openai tool specs from pocket
tool_specs = pocket.get_open_ai_tool_specs()
```


### Tool Injection

```python
import os

from openai import OpenAI

llm = OpenAI()

messages = [
    {
        "role": "user",
        "content": "get slack message",
    }
]
response = llm.chat.completions.create(
    model=os.getenv("OPEN_AI_MODEL"),
    messages=messages,
    tools=tool_specs  # pass the tool specs as an tools argument
)
```


### Tool Call

```python
response = llm.chat.completions.create(
    model=os.getenv("OPEN_AI_MODEL"),
    messages=messages,
    tools=tool_specs
)

choice = response.choices[0]
messages.append(choice.message)

if choice.finish_reason == "tool_calls":
    for tool_call in choice.message.tool_calls:
        # tool call by pocket
        tool_message = pocket.invoke(tool_call)
        messages.append(tool_message)

    # ...
```

### Full Code

```python
import os

from openai import OpenAI

import hyperpocket as pk
from pocket_openai import PocketOpenAI

pocket = PocketOpenAI(tools=[
    *pk.curated_tools.SLACK,  # SLACK = [slack_get_message, slack_post_message, ..]
    *pk.curated_tools.LINEAR,
    "https://github.com/my-org/some-awesome-tool"]
)
tool_specs = pocket.get_open_ai_tool_specs()
llm = OpenAI()
messages = [
    {
        "role": "user",
        "content": "get slack message",
    }
]
response = llm.chat.completions.create(
    model=os.getenv("OPEN_AI_MODEL"),
    messages=messages,
    tools=tool_specs
)

choice = response.choices[0]
messages.append(choice.message)

if choice.finish_reason == "tool_calls":
    for tool_call in choice.message.tool_calls:
        tool_message = pocket.invoke(tool_call)
        messages.append(tool_message)

    repsonse_after_tool_call = llm.chat.completions.create(
        model=os.getenv("OPEN_AI_MODEL"),
        messages=messages,
        tools=tool_specs
    )
```


### Examples

```python

from openai import OpenAI

import hyperpocket as pk
from pocket_openai import PocketOpenAI

pocket = PocketOpenAI(
    tools=[
        *pk.curated_tools.SLACK,  # SLACK = [slack_get_message, slack_post_message, ..]
        *pk.curated_tools.LINEAR,
        "https://github.com/my-org/some-awesome-tool"]
)
tool_specs = pocket.get_open_ai_tool_specs()

model = OpenAI()
messages = []
while True:
    print("user input(q to quit) : ", end="")
    user_input = input()
    if user_input == "q":
        break

    user_message = {"content": user_input, "role": "user"}
    messages.append(user_message)

    while True:
        response = model.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tool_specs,
        )
        choice = response.choices[0]
        messages.append(choice.message)
        if choice.finish_reason == "stop":
            break

        elif choice.finish_reason == "tool_calls":
            tool_calls = choice.message.tool_calls
            for tool_call in tool_calls:
                tool_message = pocket.invoke(tool_call)
                messages.append(tool_message)

    print("response : ", messages[-1].content)
```