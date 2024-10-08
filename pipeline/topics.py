
from include.common import *
from  include.agents.reflection_bloggers import Writer, Critic, Reviewer, Summarizer

    
import yaml


writer = Writer()
critic = Critic()  
seo_reviwer= Reviewer("SEO Reviewer")
legal_reviewer= Reviewer("Legal Reviewer")
ethics_reviewer= Reviewer("Ethics Reviewer")
meta_summarizer= Summarizer("Meta Summarizer")

chats = [
    {
        "agent": writer,
        
        "action": "generate_reply",
        "kwargs": {"task_name": "initial_task"},
        
    },
    {
        "agent": critic,        
        "action": "reflect_with_llm",
        "add_history_from": [writer],

    },
    {   #we are reusing previously defined writer here
        "agent": writer,
        
        "add_history_from": [critic],
        "action": "generate_reply",
        "kwargs": {"task_name": "revision_task"},
    },
    {   
        "agent": seo_reviwer, 
        "agent_name": "SEO Reviewer",     
        "action": "reflect_with_llm",
        "add_history_from": [writer],
    },
    {
        "agent": legal_reviewer,
        "agent_name": "Legal Reviewer",
        "action": "reflect_with_llm",
        "add_history_from": [writer],
    },
    {
        "agent": ethics_reviewer,
        "agent_name": "Ethics Reviewer",
        "action": "reflect_with_llm",
        "add_history_from": [writer],
    },
    {
        "agent": meta_summarizer,
        "agent_name": "Meta Summarizer",
        "action": "summarize",
        "add_history_from": [writer, seo_reviwer,legal_reviewer, ethics_reviewer],
    },
    {
        "agent": writer,
        
        "action": "generate_reply",
        "add_history_from": [meta_summarizer],
        "kwargs": {"task_name": "final_task"},
    }
]


