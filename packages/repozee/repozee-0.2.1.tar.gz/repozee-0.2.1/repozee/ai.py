import os
from pathlib import Path
from datetime import date
import sys
import yaml

import anthropic
from jinja2 import Template

from repozee import load_definition


class AI:

    tools = yaml.safe_load(load_definition('tools.yml'))
    system_prompt = load_definition('system.md')
    user_prompt = Template(load_definition('user.md'))

    def __init__(self, toolset=None):
        self.toolset = toolset
        self.client = anthropic.Anthropic()

    def send(self, messages: list):
        params = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "temperature": 0,
            "system": self.system_prompt,
            "messages": messages,
        }
        if self.toolset:
            params["tools"] = self.toolset.definitions
        message = self.client.messages.create(**params)
        return message

    def ask(self, template_name: str, data: dict) -> str:
        template = Template(load_definition(template_name + '.md'))
        messages = [
            {
                "role": "user",
                "content": [
                        {
                            "type": "text",
                            "text": template.render(
                                data=data,
                                today=date.today())
                        }
                ]
            }
        ]
        message = self.send(messages)
        response = next(c for c in message.content if c.type == 'text')
        return response.text

    def chat(self):
        messages = []
        while True:
            print('-'*80)
            if messages:
                question = input("\nYou: ").strip()
                print()
            else:
                question = "List"
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.user_prompt.render(
                                question=question,
                                today=date.today())
                        }
                    ]
                }
            )
            message = self.send(messages)
            while messages[-1]['role'] != 'assistant':
                for content in message.content:
                    if content.type == 'text':
                        print(content.text)
                        print()
                        messages.append({
                            "role": "assistant",
                            "content": content.text
                        })
                    elif content.type == 'tool_use':
                        if content.name == 'quit':
                            return
                        else:
                            tool = getattr(self.toolset, content.name)
                            messages.append({
                                "role": "assistant",
                                "content": [dict(content)]
                            })
                            id = content.id
                            result = str(tool(**content.input))
                            messages.append({
                                "role": "user",
                                "content": [{
                                    "type": "tool_result",
                                    "tool_use_id": id,
                                    "content": result
                                }]
                            })
                            message = self.send(messages)
