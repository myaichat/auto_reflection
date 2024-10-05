#!/usr/bin/env python
# coding: utf-8

import yaml
import autogen
from os.path import join
from pprint import pprint as pp

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setup LLM configuration
llm_config = config['llm_config']

# Set title and task using values from the YAML config
title = config['title']
task = config['task'].format(title=title)


# Create a writer agent
writer = autogen.AssistantAgent(
    name="Writer",
    system_message=config['writer_system_message'].format(title=title),
    llm_config=llm_config,
)

# Generate the initial reply from the writer agent
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
    # Get the chat messages, ensure the list is not empty
    messages = recipient.chat_messages_for_summary(sender)
    from pprint import pprint as pp
    pp(config)
    e()
    if messages:  # Check if there are any messages
        return f'''Review the following content: \n\n {messages[-1]['content']}'''
    else:
        return "No messages available for review."


# Define the review chats with function references for messages
review_chats = [
    {
     "recipient": SEO_reviewer, 
     "message": reflection_message,  # Pass the function reference, not the result
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": legal_reviewer, 
     "message": reflection_message,  # Pass the function reference
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": ethics_reviewer, 
     "message": reflection_message,  # Pass the function reference
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt": config['review_summary_prompt']},
     "max_turns": 1
    },
    {
     "recipient": meta_reviewer, 
     "message": "Aggregate feedback from all reviewers and give final suggestions on the content.", 
     "max_turns": 1
    }
]

# Processing the review chats, calling the reflection_message function dynamically
for chat in review_chats:
    if callable(chat['message']):
        # Call the message function dynamically with required parameters
        chat['message'] = chat['message'](
            recipient=chat['recipient'], 
            messages=None,  # Adjust this as needed for your case
            sender=writer, 
            config=config
        )

# Register nested chats for the critic agent
critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

# Initiate chat between writer and critic agents
res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

# Initiate final chat for reviews
res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

# Print the final result
print("Final Refined List of Blog Headline Suggestions:")
print(res.summary)
