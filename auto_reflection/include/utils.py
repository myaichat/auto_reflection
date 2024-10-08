

import yaml
from os.path import join
from pprint import pprint as pp
import importlib.util
import sys

from  .config import init_config


apc = init_config.apc


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

def execute_pipeline(title, py_pipeline_name,yaml_pprompt_config):
    apc.set_pipeline_log(py_pipeline_name, yaml_pprompt_config)

    with open(yaml_pprompt_config, 'r') as file:
        apc.data=data = yaml.safe_load(file)
    apc.llm_api=apc.data['llm_config'].get('llm_api', None)
    assert apc.llm_api, "LLM API not found in config"
    apc.vars=vars=  data['vars']
    for key, val in vars.items( ):
        if val in globals():
            vars[key] = locals()[val]
    
    pipeline= import_pipeline(py_pipeline_name)
    #exit()
    response=[]
    
    for cid, chat in enumerate(pipeline.chats):
        #pp(chat)
        apc.chat=chat
        agent=chat['agent']
        agent_name=chat.get('agent_name', None)
        if not agent_name:
            agent_name=agent.agent_name
        assert agent_name, f"Agent name not found for agent: {agent}"
        add_history_from=chat.get('add_history_from', [])
        for from_agent  in add_history_from:
            agent.add_history(from_agent.get_latest_history())
        
        
        action_method=chat['action']
        action=getattr(agent, action_method) 
        agent_kwargs=chat.get('kwargs', {})
        if_mock=chat.get('mock', False)
        print(f"if_mock: {if_mock}")
        if if_mock:
            clog=apc.mock_data[cid]
            
            
            magent=clog["agent_name"]
            
            assert magent==agent_name, f"Agent name mismatch: {magent}!={agent_name}"
            #print(cid)
            maction_method=clog['chat']["action"]
            assert maction_method==action_method, f"Action method mismatch: {maction_method}!={action_method}"
            mocked_response=clog['msg']
            #pp(mocked_response)
            agent_kwargs['mock']=clog
        
        #pp(agent_kwargs)
        #exit()
           
        response_format=chat.get('response_format', None)
        agent_kwargs['response_format']=response_format
        agent_response=action(**agent_kwargs)
        response.append(agent_response)
    
    
    return response[-1]