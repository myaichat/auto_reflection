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
        print(self.name,len(self.chat_history))
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
        print('reflection', self.name,len(self.chat_history))
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
    Write a list of 10 potential topics/headlines including "Introduction" and 'Conclusion' for future blogpost reflecting mentioned title.
    Each headline should reflect a different aspect of importance,
    and should be concise but engaging.
'''

writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer tasked with generating a list of 10 potential blog topics/headlines "
                   "including 'Introduction' and 'Conclusion' for the blogpost title: "
                   f"'{title}'. Focus on making each headline concise, engaging, and reflective of different aspects "
                   "of the blog topic.",
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

# Critic reviews and refines Writer's blog titles
reflection_prompt = "Please review the following list of blog titles and suggest improvements."
critic_response = critic.reflect_with_llm(reflection_prompt)
print("\nCritic's Response:")
print(critic_response)

# Define SEO Reviewer agent
seo_reviewer = AssistantAgent(
    name="SEO Reviewer",
    system_message="You are an SEO reviewer tasked with optimizing the list of blog titles for better search engine ranking. "
                   "Make sure the suggestions include relevant keywords, improve visibility, and are concise (within 3 bullet points).",
    llm_config=llm_config
)

# SEO Reviewer reflects on the content
seo_review_prompt = "Review the following list of blog titles for SEO optimization and suggest improvements."
seo_response = seo_reviewer.reflect_with_llm(seo_review_prompt)
print("\nSEO Reviewer's Response:")
print(seo_response)

# Define Legal Reviewer agent
legal_reviewer = AssistantAgent(
    name="Legal Reviewer",
    system_message="You are a legal reviewer tasked with ensuring that the blog titles are legally compliant and free from any issues. "
                   "Make sure your suggestions are concise (within 3 bullet points) and focus on legal concerns.",
    llm_config=llm_config
)

# Legal Reviewer reflects on the blog titles
legal_review_prompt = "Review the following list of blog titles for any legal issues and suggest improvements."
legal_response = legal_reviewer.reflect_with_llm(legal_review_prompt)
print("\nLegal Reviewer's Response:")
print(legal_response)

# Define Ethics Reviewer agent
ethics_reviewer = AssistantAgent(
    name="Ethics Reviewer",
    system_message="You are an ethics reviewer tasked with ensuring that the blog titles are ethically sound. "
                   "Make sure your suggestions are concise (within 3 bullet points) and focus on ethical concerns.",
    llm_config=llm_config
)

# Ethics Reviewer reflects on the blog titles
ethics_review_prompt = "Review the following list of blog titles for any ethical issues and suggest improvements."
ethics_response = ethics_reviewer.reflect_with_llm(ethics_review_prompt)
print("\nEthics Reviewer's Response:")
print(ethics_response)

# Define Meta Reviewer agent
meta_reviewer = AssistantAgent(
    name="Meta Reviewer",
    system_message="You are a meta reviewer tasked with aggregating feedback from the SEO, Legal, and Ethics reviewers "
                   "and providing a final, refined list of blog titles.",
    llm_config=llm_config
)

# Meta Reviewer aggregates all feedback and refines the blog titles
meta_review_prompt = f"Based on the following reviews:\n\nSEO Review:\n{seo_response}\n\nLegal Review:\n{legal_response}\n\nEthics Review:\n{ethics_response}\n\nProvide a final refined list of blog titles."
meta_response = meta_reviewer.reflect_with_llm(meta_review_prompt)

# Output the final refined list of blog headline suggestions
print("\nFinal Refined List of Blog Headline Suggestions (from Meta Reviewer):")
print(meta_response)
