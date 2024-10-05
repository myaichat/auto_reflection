from openai import OpenAI

class AssistantAgent:
    def __init__(self, name, system_message, llm_config):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.chat_history = []
        self.client = OpenAI()  # Initialize the OpenAI client

    def generate_reply(self, messages):
        # Append user message to chat history
        self.chat_history.append({"role": "user", "content": messages[0]["content"]})
        
        # Generate response from the LLM using the updated API
        response = self.client.chat.completions.create(
            model=self.llm_config["model"],
            messages=[
                {"role": "system", "content": self.system_message},
                *self.chat_history
            ]
        )
        
        # Append assistant message to chat history
        assistant_message = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

    def reflect_with_llm(self, reflection_prompt):
        # Generate reflection based on the conversation history
        reflection_message = {
            "role": "user",
            "content": reflection_prompt
        }
        response = self.client.chat.completions.create(
            model=self.llm_config["model"],
            messages=[
                {"role": "system", "content": self.system_message},
                *self.chat_history,
                reflection_message  # Add reflection prompt at the end
            ]
        )
        return response.choices[0].message.content
    
    def get_summary(self):
        # A simple summary of the last message in the chat history
        if self.chat_history:
            return self.chat_history[-1]['content']
        else:
            return "No conversation to summarize."


# Usage
llm_config = {"model": "gpt-3.5-turbo"}

# Define an agent
writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write 10 potential topics/headlines for a blogpost.",
    llm_config=llm_config
)

# Task for the writer
task = '''
    Assuming the blog title is: "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
    Write a list of 10 potential topics/headlines including "Introduction" and 'Conclusion' for future blogpost reflecting the mentioned title.
    Each headline should reflect a different aspect of importance and should be concise but engaging.
'''

# Writer generates a reply
initial_response = writer.generate_reply([{"content": task, "role": "user"}])
print("Writer's Response:")
print(initial_response)

# Now we ask the agent to reflect on its generated reply
reflection_prompt = "Can you reflect on the generated headlines and provide suggestions for improvement?"

# Generate reflection based on the previous conversation
reflection_response = writer.reflect_with_llm(reflection_prompt)
print("Reflection from LLM:")
print(reflection_response)
