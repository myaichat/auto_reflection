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


# Define the critic agent
class CriticAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        system_message = "You are a critic. Review the content provided and give constructive feedback to improve the quality."
        super().__init__(name, system_message, llm_config)
        
# Define the SEO agent
class SEOAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        system_message = "You are an SEO reviewer. Optimize the content for better search engine ranking in 3 concise points."
        super().__init__(name, system_message, llm_config)

# Define the Legal agent
class LegalAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        system_message = "You are a legal reviewer. Ensure that the content is legally compliant and suggest improvements in 3 concise points."
        super().__init__(name, system_message, llm_config)

# Define the Ethics agent
class EthicsAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        system_message = "You are an ethics reviewer. Ensure that the content is ethically sound and suggest improvements in 3 concise points."
        super().__init__(name, system_message, llm_config)

# Define the Meta reviewer agent
class MetaAgent(AssistantAgent):
    def __init__(self, name, llm_config):
        system_message = "You are a meta reviewer. Aggregate the feedback from all other reviewers and provide a final suggestion."
        super().__init__(name, system_message, llm_config)


# Function to orchestrate the review process
def orchestrate_review(writer, critic, seo_reviewer, legal_reviewer, ethics_reviewer, meta_reviewer):
    # Writer generates initial reply
    initial_response = writer.generate_reply([{"content": task, "role": "user"}])
    print("Writer's Initial Response:")
    print(initial_response)

    # Critic reviews the content
    critic_response = critic.initiate_chat(writer, initial_response, max_turns=2)
    print("Critic's Response:")
    print(critic_response)

    # SEO reviews the content
    seo_response = seo_reviewer.initiate_chat(writer, initial_response, max_turns=1)
    print("SEO's Response:")
    print(seo_response)

    # Legal reviews the content
    legal_response = legal_reviewer.initiate_chat(writer, initial_response, max_turns=1)
    print("Legal's Response:")
    print(legal_response)

    # Ethics reviews the content
    ethics_response = ethics_reviewer.initiate_chat(writer, initial_response, max_turns=1)
    print("Ethics's Response:")
    print(ethics_response)

    # Meta reviews and aggregates the feedback
    meta_response = meta_reviewer.initiate_chat(writer, initial_response, max_turns=1)
    print("Meta Reviewer's Final Suggestion:")
    print(meta_response)


# Configuration for LLM
llm_config = {"model": "gpt-3.5-turbo"}

# Define agents
writer = AssistantAgent(name="Writer", system_message="You are a writer. You write 10 potential topics/headlines for a blogpost.", llm_config=llm_config)
critic = CriticAgent(name="Critic", llm_config=llm_config)
seo_reviewer = SEOAgent(name="SEO Reviewer", llm_config=llm_config)
legal_reviewer = LegalAgent(name="Legal Reviewer", llm_config=llm_config)
ethics_reviewer = EthicsAgent(name="Ethics Reviewer", llm_config=llm_config)
meta_reviewer = MetaAgent(name="Meta Reviewer", llm_config=llm_config)

# Task message
title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
task = f'''
        Assuming blog title is: "{title}"
        Write a list of 10 potential topics/headlines including "Introduction" and 'Conclusion' for future blogpost reflecting mentioned title.
        Each headline should reflect a different aspect of importance,
        and should be concise but engaging.
        The result should be a list of 10 potential blog post sections/titles.
       '''

# Orchestrate reviews
orchestrate_review(writer, critic, seo_reviewer, legal_reviewer, ethics_reviewer, meta_reviewer)
