import openai

class AssistantAgent:
    def __init__(self, name, system_message, llm_config):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.chat_history = []

    def generate_reply(self, messages):
        # Append user message to chat history
        self.chat_history.append({"role": "user", "content": messages[0]["content"]})
        
        # Generate response from the LLM
        response = openai.ChatCompletion.create(
            model=self.llm_config["model"],
            messages=[
                {"role": "system", "content": self.system_message},
                *self.chat_history
            ]
        )
        
        # Append assistant message to chat history
        self.chat_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        return response['choices'][0]['message']['content']
    
    def initiate_chat(self, recipient, message, max_turns, summary_method=None):
        # Initiate a conversation with another agent
        response = recipient.generate_reply([{"content": message, "role": "user"}])
        self.chat_history.append({"role": recipient.name, "content": response})
        return response

    def get_summary(self):
        # Return a summary of the latest conversation
        if self.chat_history:
            return self.chat_history[-1]['content']
        else:
            return "No conversation to summarize."
