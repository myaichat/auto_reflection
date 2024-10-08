
from auto_reflection.include.common import *
from  auto_reflection.include.agents.reflection_bloggers import Writer, Critic, Reviewer, Summarizer

    
import yaml


writer = Writer()
critic = Critic()  
seo_reviwer= Reviewer("SEO Reviewer")
legal_reviewer= Reviewer("Legal Reviewer")
ethics_reviewer= Reviewer("Ethics Reviewer")
meta_summarizer= Summarizer("Meta Summarizer")
mocked=True
chats = [
    {
        "agent": writer,
        
        "action": "generate_reply",
        "kwargs": {"task_name": "initial_task"},
        "mock": mocked,
    },
    {
        "agent": critic,    
             
        "action": "reflect_with_llm",
        "add_history_from": [writer],
        "mock": mocked,
    },
    {   #we are reusing previously defined writer here
        "agent": writer,
         
        "add_history_from": [critic],
        "action": "generate_reply",
        "kwargs": {"task_name": "revision_task"},
        "mock": mocked,
    },
    {   
        "agent": seo_reviwer, 
        "agent_name": "SEO Reviewer",     
        "action": "reflect_with_llm",
        "add_history_from": [writer],
        "mock": mocked,
    },
    {
        "agent": legal_reviewer,
        "agent_name": "Legal Reviewer",
        "action": "reflect_with_llm",
        "add_history_from": [writer],
        "mock": mocked,
    },
    {
        "agent": ethics_reviewer,
        "agent_name": "Ethics Reviewer",
        "action": "reflect_with_llm",
        "add_history_from": [writer],
        "mock": mocked,
    },
    {
        "agent": meta_summarizer,
        "agent_name": "Meta Summarizer",
        "action": "summarize",
        "add_history_from": [writer, seo_reviwer,legal_reviewer, ethics_reviewer],
        "mock": mocked,
    },
    {
        "agent": writer,        
        "action": "generate_reply",
        "add_history_from": [meta_summarizer],
        "kwargs": {"task_name": "final_task"},
        "mock": True,
        
        'response_format' : {
            "type": "json_schema",
            "json_schema": {
                "name": "section",
                "schema": {
                    "type": "object",
                    "properties": {
                        "section": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["section"]
                }
            }
        }
    }
    
]


