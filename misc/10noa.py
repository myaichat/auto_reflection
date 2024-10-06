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
    Write a list of 5 potential topics/headlines including "Introduction" and 'Conclusion' for future blogpost reflecting mentioned title.
    Each headline should reflect a different aspect of importance,
    and should be concise but engaging.
'''

writer = AssistantAgent(
    name="Writer",
    system_message="You are a writer tasked with generating a list of 5 potential blog topics/headlines "
                   "including 'Introduction' and 'Conclusion' for the blogpost title: "
                   f"'{title}'. Focus on making each headline concise, engaging, and reflective of different aspects "
                   "of the blog topic.",
    llm_config=llm_config
)

# Writer generates initial list of blog headlines
initial_response = writer.generate_reply([{"content": task, "role": "user"}])
print("Initial Writer Response:")
print(initial_response)

# Define Critic agent to focus on refining blog titles and reviewing the writer's work
critic = AssistantAgent(
    name="Critic",
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive feedback to help improve the quality of the content.",
    llm_config=llm_config
)

critic.chat_history.append({"role": "user", "content": task})

# Critic reviews the Writer's response (pass writer's response as part of the chat history)
critic.chat_history.append({"role": "assistant", "content": initial_response})

# Critic reviews and refines Writer's blog titles
reflection_prompt = "Please review the following list of blog titles and suggest improvements"
critic_response = critic.reflect_with_llm(reflection_prompt)
print("\nCritic's Response:")
print(critic_response)




# Define SEO Reviewer agent
seo_reviewer = AssistantAgent(
    name="SEO Reviewer",
    system_message="You are an SEO reviewer, known for your ability to optimize content for search engines, "
        "ensuring that it ranks well and attracts organic traffic. "
        "Make sure your suggestion is concise (within 3 bullet points), concrete and to the point. "
        "Begin the review by stating your role.",
    llm_config=llm_config
)

seo_reviewer.chat_history.append({"role": "user", "content": task})

# Critic reviews the Writer's response (pass writer's response as part of the chat history)
seo_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

# SEO Reviewer reflects on the content
seo_review_prompt = "Review the writer's initial responce for SEO optimization and suggest improvements."
seo_response = seo_reviewer.reflect_with_llm(seo_review_prompt)
print("\nSEO Reviewer's Response:")
print(seo_response)


# Define Legal Reviewer agent
legal_reviewer = AssistantAgent(
    name="Legal Reviewer",
    system_message="You are a legal reviewer, known for your ability to ensure that content is legally compliant "
        "and free from any potential legal issues. "
        "Make sure your suggestion is concise (within 3 bullet points), concrete and to the point. "
        "Begin the review by stating your role.",
    llm_config=llm_config
)

legal_reviewer.chat_history.append({"role": "user", "content": task})

# Critic reviews the Writer's response (pass writer's response as part of the chat history)
legal_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

# Legal Reviewer reflects on the blog titles
legal_review_prompt = "Review the writer's initial responce for any legal issues and suggest improvements"
legal_response = legal_reviewer.reflect_with_llm(legal_review_prompt)
print("\nLegal Reviewer's Response:")
print(legal_response)

# Define Ethics Reviewer agent
ethics_reviewer = AssistantAgent(
    name="Ethics Reviewer",
    system_message="You are an ethics reviewer, known for your ability to ensure that content is ethically sound "
        "and free from any potential ethical issues. "
        "Make sure your suggestion is concise (within 3 bullet points), concrete and to the point. "
        "Begin the review by stating your role.",
    llm_config=llm_config
)

legal_reviewer.chat_history.append({"role": "user", "content": task})

# Critic reviews the Writer's response (pass writer's response as part of the chat history)
legal_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

# Ethics Reviewer reflects on the blog titles
ethics_review_prompt = "Review writer's initia; response for any ethical issues and suggest improvements."
ethics_response = ethics_reviewer.reflect_with_llm(ethics_review_prompt)
print("\nEthics Reviewer's Response:")
print(ethics_response)

# Define Meta Reviewer agent
meta_reviewer = AssistantAgent(
    name="Meta Reviewer",
    system_message="You are a meta reviewer tasked with aggregating feedback from the SEO, Legal, and Ethics reviewers "
                   "and providing a **final refined list of blog titles** after incorporating all their suggestions.",
    llm_config=llm_config
)

meta_reviewer.chat_history.append({"role": "user", "content": task})

# Critic reviews the Writer's response (pass writer's response as part of the chat history)
legal_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

meta_reviewer.chat_history.append({"role": "assistant", "content": f"Critic's Feedback: {critic_response}"})
# Append feedback to Meta Reviewer's chat history with reviewer names
meta_reviewer.chat_history.append({"role": "assistant", "content": f"SEO Reviewer Feedback:\n{seo_response}"})
meta_reviewer.chat_history.append({"role": "assistant", "content": f"Legal Reviewer Feedback:\n{legal_response}"})
meta_reviewer.chat_history.append({"role": "assistant", "content": f"Ethics Reviewer Feedback:\n{ethics_response}"})



# Meta Reviewer aggregates all feedback and refines the blog titles
meta_review_prompt = "Please refine the Writer's initial response  based on the feedback provided by the Critic, SEO, Legal, and Ethics reviewers."

meta_response = meta_reviewer.reflect_with_llm(meta_review_prompt)
print("\nMeta Reviewer's Refined Response:")
print(meta_response)
