
import yaml
from    os.path import join
from   pprint import pprint as pp   

from include.common import *



import  include.config.init_config as  init_config

init_config.init(**{})
apc = init_config.apc

apc.verbose = True
import importlib.util
import sys
def import_pipeline(pipeline_name):
 

    # Specify the path to the module (Python file)
    module_name = "pipeline"
    file_path = join("pipeline", pipeline_name+".py" )   

    # Load the module from the file path
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)   
    return module 

def execute_pipeline(title, pipeline_name,config):


    with open(config, 'r') as file:
        apc.data=data = yaml.safe_load(file)

    apc.vars=vars=  data['vars']
    for key, val in vars.items( ):
        if val in globals():
            vars[key] = locals()[val]
    
    pipeline= import_pipeline(pipeline_name)
    response=[]
    for chat in pipeline.chats:
        pp(chat)
        agent=chat['agent']
        add_history_from=chat.get('add_history_from', [])
        for from_agent  in add_history_from:
            agent.add_history(from_agent.get_latest_history())
        
        
        action_method=chat['action']
        action=getattr(agent, action_method) 
        agent_kwargs=chat.get('kwargs', {})
        agent_response=action(**agent_kwargs)
        response.append(agent_response)
        

  
    return response[1]


if __name__ == '__main__':
    py_pipeline_config='blog_writer'

    yaml_pipeline_config=join('config','topics.yaml')

    title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
    execute_pipeline(title, py_pipeline_config, yaml_pipeline_config)
