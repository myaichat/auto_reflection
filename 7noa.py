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
        print(self.name, len(self.chat_history))
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
        print('reflection', self.name, len(self.chat_history))
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

# Configuration for LLM
llm_config = {"model": "gpt-3.5-turbo"}

# Define Writer agent to focus on generating blog titles
title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
task = f'''
    Assuming blog title is: "{title}"
    Write a list of 510 potential topics/headlines including "Introduction" and 'Conclusion' for future blogpost reflecting mentioned title.
    Each headline should reflect a different aspect of importance,
    and should be concise but engaging.
'''

writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer. You Write a list of 10 potential topics/headlines including 'Introduction' "
        f"and 'Conclusion' for future blogpost reflecting thiss title : '{title}'"
        "Each headline should reflect a different aspect of importance,"
        "and should be concise but engaging. You must polish your "
        "writing based on the feedback you receive and give a refined "
        "version. Only return your final work without additional comments.",
    llm_config=llm_config
)

# Writer generates initial list of blog headlines
initial_response = writer.generate_reply([{"content": task, "role": "user"}])
print("Initial Writer Response:")
print(initial_response)

# Define Critic agent to focus on refining blog titles
critic = AssistantAgent(
    name="Critic",
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive feedback to help improve the quality of the content.",
    llm_config=llm_config
)

# Critic reviews and refines Writer's blog titles, passing the writer's response
reflection_prompt = f"Please review the following list of blog titles and suggest improvements:\n\n{initial_response}"
critic_response = critic.reflect_with_llm(reflection_prompt)
print("\nCritic's Response:")
print(critic_response)
