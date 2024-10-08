#!/usr/bin/env python
# coding: utf-8

import yaml
import autogen
from os import path

# Load configuration from YAML file
with open(join('config','titles.yaml'), 'r') as file:
    config = yaml.safe_load(file)

# Setup
llm_config = {"model": "gpt-3.5-turbo"}
llm_config = {"model": "gpt-4o-mini"}

parsed=config['writer_system_message'].format(title=config['title'])
print(parsed)   
exit()
# Create a writer agent
writer = autogen.AssistantAgent(
    name="Writer",
    system_message=config['writer_system_message'].format(title=config['title']),
    llm_config=llm_config,
)

# Generate initial reply
task = config['task'].format(title=config['title'])

reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])

print("Initial Writer Response:")
print(reply)

# Create a critic agent
critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message=config['critic_system_message'],
)

# Initiate chat between writer and critic
res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

# Create reviewer agents
SEO_reviewer = autogen.AssistantAgent(
    name="SEO Reviewer",
    llm_config=llm_config,
    system_message=config['seo_reviewer_system_message'],
)

legal_reviewer = autogen.AssistantAgent(
    name="Legal Reviewer",
    llm_config=llm_config,
    system_message=config['legal_reviewer_system_message'],
)

ethics_reviewer = autogen.AssistantAgent(
    name="Ethics Reviewer",
    llm_config=llm_config,
    system_message=config['ethics_reviewer_system_message'],
)

meta_reviewer = autogen.AssistantAgent(
    name="Meta Reviewer",
    llm_config=llm_config,
    system_message=config['meta_reviewer_system_message'],
)

# Define reflection message function
def reflection_message(recipient, messages, sender, config):
    return config['reflection_message'].format(recipient=recipient, sender=sender)

# Set up review chats
review_chats = [
    {
     "recipient": SEO_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": legal_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": ethics_reviewer, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": meta_reviewer, 
     "message": "Aggregate feedback from all reviewers and give final suggestions on the content.", 
     "max_turns": 1
    },
]

# Register nested chats
critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

# Initiate final chat
res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

# Print final result
print("Final Refined List of Blog Headline Suggestions:")
print(res.summary)