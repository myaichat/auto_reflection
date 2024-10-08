from openai import OpenAI
from pprint import pprint as pp

class AssistantAgent:
    def __init__(self, name, system_message, llm_config):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.chat_history = []
        self.client = OpenAI()  # Initialize the OpenAI client

    def generate_reply(self, task, mocked_response=None, return_format=None):
        # Append user message to chat history
        print(self.name, len(self.chat_history))
        
        self.chat_history.append({"role": "user", "content": task})
        
        # Generate response from the LLM using the updated API
        format={}
        if return_format:
            format = {
                    'response_format' : {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "titles",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "titles": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },
                            "required": ["titles"]
                        }
                    }
                }
            }
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history
                ],
            **format

            )
            

            

            # Append assistant message to chat history
            assistant_message = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

    def reflect_with_llm(self, reflection_prompt, mocked_response=None, return_format=None):
        # Generate reflection based on the conversation history
        print('reflection', self.name, len(self.chat_history))
        reflection_message = {
            "role": "user",
            "content": reflection_prompt
        }
        format={}
        if return_format:
            format = {
                    'response_format' : {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "titles",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "titles": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },
                            "required": ["titles"]
                        }
                    }
                }
            }
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history,
                    reflection_message  # Add reflection prompt at the end
                ],
                **format
            )
            assistant_message=response.choices[0].message.content
        return assistant_message

    def summarize(self, summary_prompt, mocked_response=None, return_format=None):
        # Generate reflection based on the conversation history
        print('summary', self.name, len(self.chat_history))
        summarization_message = {
            "role": "user",
            "content": summary_prompt
        }
        format={}
        if return_format:
            format = {
                    'response_format' : {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "topics",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "topics": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },
                            "required": ["topics"]
                        }
                    }
                }
            }        
        if mocked_response:
            assistant_message=mocked_response
        else:
            response = self.client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.chat_history,
                    summarization_message  # Add reflection prompt at the end
                ],
                **format
            )
            assistant_message=response.choices[0].message.content
        return assistant_message