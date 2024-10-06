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
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        #self.task = task    
        self.agent_response = None
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
    def add_history(self, messages):
        self.agent.chat_history += messages        
    def generate_reply(self, task):
        agent_response= self.agent.generate_reply([{"content": task, "role": "user"}])    
        if self.verbose:  
            resp(agent_response, f'Initial {self.agent_name} Response:')
        self.agent_response = agent_response
        return agent_response
    
if 1:
    writer = Writer(data, vars, verbose=True)
    initial_response = writer.generate_reply(task)



class Critic():
    def __init__(self, data, vars, receiever, verbose=False):
        self.verbose=verbose
        self.receiever = receiever
        #self.recepient = recepient
        self.agent_name=agent_name="Critic"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self):


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        self.receiever.add_history([{"role": "assistant", "content": f"{self.agent_name} Feedback:\n{agent_response}"}])
        return agent_response    
    

if 1:
    task_msg={"role": "user", "content": task}
    writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
    critic = Critic(data, vars,receiever=writer, verbose=True)
    critic.add_history([task_msg, writer_msg])
    critic_response = critic.reflect_with_llm()
#exit()


class SEO_Reviewer():
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name="SEO Reviewer"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self):


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        
        return agent_response 
    

if 1:
    #task_msg={"role": "user", "content": task}
    #writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
    seo_reviewer = SEO_Reviewer(data, vars, verbose=True)
    seo_reviewer.add_history([task_msg, writer_msg])
    seo_reviewer_response = seo_reviewer.reflect_with_llm()
#exit()


class Legal_Reviewer():
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name="Legal Reviewer"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self):


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        
        return agent_response 

if 1:
    #task_msg={"role": "user", "content": task}
    #writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
    legal_reviewer = Legal_Reviewer(data, vars, verbose=True)
    legal_reviewer.add_history([task_msg, writer_msg])
    legal_reviewer_response = legal_reviewer.reflect_with_llm()
#exit()


class Ethics_Reviewer():
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name="Ethics Reviewer"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self):


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        
        return agent_response 

if 1:
    #task_msg={"role": "user", "content": task}
    #writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
    ethics_reviewer = Ethics_Reviewer(data, vars, verbose=True)
    ethics_reviewer.add_history([task_msg, writer_msg])
    ethics_reviewer_response = ethics_reviewer.reflect_with_llm()




class Meta_Reviewer():
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name="Meta Reviewer"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self):


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        
        return agent_response 
    
if 1:
    #task_msg={"role": "user", "content": task}
    #writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
    #meta_reviewer.chat_history.append({"role": "assistant", "content": f"Critic's Feedback: {critic_response}"})
    # Append feedback to Meta Reviewer's chat history with reviewer names
    seo_msg ={"role": "assistant", "content": f"SEO Reviewer Feedback:\n{seo_reviewer.agent_response}"}
    legal_msg ={"role": "assistant", "content": f"Legal Reviewer Feedback:\n{legal_reviewer.agent_response}"}
    ethics_msg ={"role": "assistant", "content": f"Ethics Reviewer Feedback:\n{ethics_reviewer.agent_response}"}
        
    meta_reviewer = Meta_Reviewer(data, vars, verbose=True)
    meta_reviewer.add_history([task_msg, writer_msg, seo_msg, legal_msg, ethics_msg])
    meta_reviewer_response = meta_reviewer.reflect_with_llm()
exit()
