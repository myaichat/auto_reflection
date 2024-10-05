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
    system_message="You are a writer. You Write a list of 5 potential topics/headlines including 'Introduction' "
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
    system_message="You are a critic. You review the work of the writer and provide constructive feedback "
                   "to help improve the quality of the content. You should be aware of the original task given to the writer.",
    llm_config=llm_config
)
if 1:   #Critique Task
    # Critic reviews and refines Writer's blog titles with the original task for context
    reflection_prompt = f"The original task for the writer was:\n\n{task}\n\n" \
                        f"Here is the writer's response:\n\n{initial_response}\n\n" \
                        "Please review the following list of blog titles and suggest improvements."
    critic_response = critic.reflect_with_llm(reflection_prompt)
    print("\nCritic's Response:")
    print(critic_response)
    # Critic's feedback is generated here as per the earlier step

if 0: # Refinement Task
    # Feed the critic's response back to the writer for refinement
    refinement_task = f"""
    The critic provided the following feedback on your work:

    {critic_response}

    Please refine your original list of blog titles based on this feedback and return the improved version.
    """

    writer_refined_response = writer.generate_reply([{"content": refinement_task, "role": "user"}])
    print("\nRefined Writer Response:")
    print(writer_refined_response)

writer_refined_response= initial_response
if 1: # SEO Reviewer
    seo_reflection_prompt = f"""
    Review the following content and provide suggestions to optimize it for search engines:
Original user prompt/question:
{task}    
    Writer initial responce:
    {writer_refined_response}
Critic responce:
{critic_response}
    """

    # SEO Reviewer gives concise feedback on how to improve the content's SEO
    seo_reviewer = AssistantAgent(
        name="SEO Reviewer",
        llm_config=llm_config,
        system_message="You are an SEO reviewer, known for your ability to optimize content for search engines, "
                    "ensuring that it ranks well and attracts organic traffic. "
                    "Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point. "
                    "Begin the review by stating your role."
    )

    seo_feedback = seo_reviewer.reflect_with_llm(seo_reflection_prompt)
    print("\nSEO Reviewer's Response:")
    print(seo_feedback)

if 1: # Legal Reviewer
    legal_reflection_prompt = f"""
    Review the following content and provide suggestions to optimize it from legal perspective:
The original task for the writer was:\n\n{task}\n\n   
    Writer initial responce:
    {writer_refined_response}
Critic responce:
{critic_response}
    """

    # In[9]:
    legal_reviewer = AssistantAgent(
        name="Legal Reviewer",
        llm_config=llm_config,
        system_message="You are a legal reviewer, known for your ability to ensure that content is legally compliant "
            "and free from any potential legal issues. "
            "Make sure your suggestion is concise (within 3 bullet points), concrete and to the point. "
            "Begin the review by stating your role.",
    )

    legal_feedback = legal_reviewer.reflect_with_llm(legal_reflection_prompt)
    print("Legal Reviewer's Response:")
    print(legal_feedback)



if 1: # Legal Reviewer
    ethics_reflection_prompt = f"""
    Review the following content and provide suggestions to optimize it from ethics perspective:
The original task for the writer was:\n\n{task}\n\n   
    Writer initial responce:
    {writer_refined_response}
Critic responce:
{critic_response}
    """

    # In[9]:
    ethics_reviewer = AssistantAgent(
        name="Ethics Reviewer",
        llm_config=llm_config,
        system_message="You are an ethics reviewer, known for your ability to ensure that content is ethically sound "
            "and free from any potential ethical issues. "
            "Make sure your suggestion is concise (within 3 bullet points), concrete and to the point. "
            "Begin the review by stating your role.",
    )

    ethics_feedback = ethics_reviewer.reflect_with_llm(ethics_reflection_prompt)
    print("Ethics Reviewer's Response:")
    print(ethics_feedback)


if 1: # Legal Reviewer
    meta_reflection_prompt = f"""
    Aggregate feedback from all reviewers and give final suggestions on the content.
The original task for the writer was:\n\n{task}\n\n

    Writer's initial and critic  Response on which feedback was provided:
    Writer initial responce:
    {writer_refined_response}
Critic responce:
{critic_response}

    The SEO Reviewer provided the following feedback on your work:

    {seo_feedback}

    The Legal Reviewer provided the following feedback on your work:

    {legal_feedback}

    The Ethics Reviewer provided the following feedback on your work:

    {ethics_feedback}
    """

    # In[9]:
    meta_reviewer = AssistantAgent(
        name="Meta Reviewer",
        llm_config=llm_config,
        system_message="You are a meta reviewer, you aggregate and review "
        "the work of other reviewers and give a final suggestion on the content.",
    )

    meta_feedback = meta_reviewer.reflect_with_llm(meta_reflection_prompt)
    print("Ethics Reviewer's Response:")
    print(meta_feedback)



# In[11]:







if 0: # Refinement Task post SEO
    # Feed the critic's response back to the writer for refinement
    refinement_task = f"""
    The SEO Reviewer provided the following feedback on your work:

    {seo_feedback}

    The Legal Reviewer provided the following feedback on your work:

    {legal_feedback}

    The Ethics Reviewer provided the following feedback on your work:

    {ethics_feedback}

    Please refine your original list of blog titles based on this feedback and return the improved version.
    """

    refined_response = writer.generate_reply([{"content": refinement_task, "role": "user"}])
    print("\nRefined post SEO/Legal/Ethics  Writer Response:")
    print(refined_response)
