from include.common import *
from include.agents import AssistantAgent  
class Writer():
    def __init__(self, data, vars,  verbose=False):
        self.verbose=verbose
        #self.task = task    
        self.agent_response = None
        self.agent_name=agent_name="Writer"
        self.writer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.writer_sysmsg, f"{self.agent_name}  system prompt")
        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.writer_sysmsg,
            llm_config=llm_config
        )  
        #self.writer.chat_history.append({"role": "user", "content": task})
        self.history=[]
    def add_history(self, messages):
        self.agent.chat_history += messages        
    def generate_reply(self, task):
        agent_response= self.agent.generate_reply(task)    
        self.history.append(agent_response)
        if self.verbose:  
            resp(agent_response, f'{self.agent_name} Response #{len(self.history)}:')
        self.agent_response = agent_response
        return agent_response
    
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
        llm_config = data['llm_config']
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
    
class Reviewer():
    def __init__(self,agent_name,  data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")

        llm_config = data['llm_config']
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
    
class Summarizer():
    def __init__(self, agent_name, data, vars,  verbose=False):
        self.verbose=verbose
        
        #self.recepient = recepient
        self.agent_name=agent_name
        self.summary_prompt = data['agents'][agent_name]['summary_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def summarize(self):


        agent_response= self.agent.summarize(self.summary_prompt)    
        if self.verbose:  
            resp(agent_response, f'{self.agent_name}''s Response:')
        self.agent_response = agent_response
        
        return agent_response 