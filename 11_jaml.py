from    os.path import join
from   pprint import pprint as pp   
import rich
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from openai import OpenAI
#style="grey", style="bold blue", style="italic yellow", style="underline green".
#border_style="bold red", border_style="#FF5733", or border_style="cyan".
#box=rich.box.ROUNDED, box=rich.box.SQUARE, box=rich.box.MINIMAL
console = Console()

def resp(msg, title):
    console.print(Panel(msg, title=title, title_align="left", border_style="cyan", 
                    style="#FF5733", box=rich.box.ROUNDED))
def promp(msg, title):
    console.print(Panel(msg, title=title, title_align="left", border_style="white", style="underline green", 
                    box=rich.box.MINIMAL, highlight=True))
        
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

import yaml

with open(join('config','topics.yaml'), 'r') as file:
    data = yaml.safe_load(file)

#pp(data)
# Configuration for LLM
#llm_config = data['llm_config']
#llm_config = {"model": "gpt-3.5-turbo"}
llm_config = data['llm_config']
# Define Writer agent to focus on generating blog titles
vars=  data['vars']

title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"

for key, val in vars.items( ):
    if val in globals():
        vars[key] = globals()[val]
pp(vars)

task = data['task'].format(**vars)
console.print(task, style="bold yellow")

class Writer():
    def __init__(self, data, vars, verbose=False):
        self.verbose=verbose
        self.agent_name=agent_name="Writer"
        self.writer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.writer_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.writer_sysmsg,
            llm_config=llm_config
        )  
        #self.writer.chat_history.append({"role": "user", "content": task})
    def generate_reply(self, task):
        initial_response= self.agent.generate_reply([{"content": task, "role": "user"}])    
        if self.verbose:  
            resp(initial_response, f'Initial {self.agent_name} Response:')
        return initial_response
    
if 1:
    writer = Writer(data, vars, verbose=True)
    initial_response = writer.generate_reply(task)
exit()

if 1:
    # Define Critic agent to focus on refining blog titles and reviewing the writer's work
    agent_name="Critic"
    critic_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
    promp(critic_sysmsg, "Critic system prompt")

    critic = AssistantAgent(
        name=agent_name,
        system_message=critic_sysmsg,
        llm_config=llm_config
    )

    critic.chat_history.append({"role": "user", "content": task})

    # Critic reviews the Writer's response (pass writer's response as part of the chat history)
    #critic.chat_history.append({"role": "assistant", "content": initial_response})
    critic.chat_history.append({"role": "assistant", "content": f'List of topics returned by writer:\n\n{initial_response}\n\n'})

    # Critic reviews and refines Writer's blog titles
    reflection_prompt = data['agents'][agent_name]['reflection_prompt']
    critic_response = critic.reflect_with_llm(reflection_prompt)

    resp(critic_response, 'Critic''s Response:')



if 1:
    agent_name="SEO Reviewer"
    seo_reviewer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
    promp(seo_reviewer_sysmsg, "SEO Reviewer system prompt")

    # Define SEO Reviewer agent
    seo_reviewer = AssistantAgent(
        name=agent_name,
        system_message=seo_reviewer_sysmsg,
        llm_config=llm_config
    )

    seo_reviewer.chat_history.append({"role": "user", "content": task})

    # Critic reviews the Writer's response (pass writer's response as part of the chat history)
    seo_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

    # SEO Reviewer reflects on the content
    reflection_prompt = data['agents'][agent_name]['reflection_prompt']
    seo_response = seo_reviewer.reflect_with_llm(reflection_prompt)
    resp(seo_response, 'SEO Reviewer''s Response:')



if 1:
    agent_name="Legal Reviewer"
    legal_reviewer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
    promp(legal_reviewer_sysmsg, "SEO Reviewer system prompt")

    # Define Legal Reviewer agent
    legal_reviewer = AssistantAgent(
        name=agent_name,
        system_message=legal_reviewer_sysmsg,
        llm_config=llm_config
    )

    legal_reviewer.chat_history.append({"role": "user", "content": task})

    # Critic reviews the Writer's response (pass writer's response as part of the chat history)
    legal_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

    # Legal Reviewer reflects on the blog titles
    
    reflection_prompt = data['agents'][agent_name]['reflection_prompt']
    legal_response = legal_reviewer.reflect_with_llm(reflection_prompt)

    resp(legal_response, 'Legal Reviewer''s Response:')

if 1:
    agent_name="Ethics Reviewer"
    ethics_reviewer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
    promp(ethics_reviewer_sysmsg, "Ethics Reviewer system prompt")

    # Define Ethics Reviewer agent
    ethics_reviewer = AssistantAgent(
        name=agent_name,
        system_message=ethics_reviewer_sysmsg,
        llm_config=llm_config
    )

    legal_reviewer.chat_history.append({"role": "user", "content": task})

    # Critic reviews the Writer's response (pass writer's response as part of the chat history)
    legal_reviewer.chat_history.append({"role": "assistant", "content": f'Writer''s initial respose:{initial_response}'})

    # Ethics Reviewer reflects on the blog titles
    
    reflection_prompt = data['agents'][agent_name]['reflection_prompt']
    ethics_response = ethics_reviewer.reflect_with_llm(reflection_prompt)

    resp(ethics_response, 'Ethics Reviewer''s Response:')

if 1:
    agent_name="Meta Reviewer"
    meta_reviewer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
    promp(meta_reviewer_sysmsg, "Meta Reviewer system prompt")

    # Define Meta Reviewer agent
    meta_reviewer = AssistantAgent(
        name=agent_name,
        system_message=meta_reviewer_sysmsg,
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
    
    reflection_prompt = data['agents'][agent_name]['reflection_prompt']
    meta_response = meta_reviewer.reflect_with_llm(reflection_prompt)

    resp(meta_response, 'Meta Reviewer''s Response:')
