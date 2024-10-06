from    os.path import join
from   pprint import pprint as pp   

from include.common import *
from  include.bloggers import Writer, Critic, Reviewer, Summarizer

    
import yaml










def generate_topics(title, config):


    with open(config, 'r') as file:
        data = yaml.safe_load(file)

    vars=  data['vars']
    for key, val in vars.items( ):
        if val in globals():
            vars[key] = locals()[val]
    pp(vars)

    task = data['agents']['Writer']['task'].format(**vars)
    console.print(task, style="bold yellow")

        
    if 1:
        writer = Writer(data, vars, verbose=True)
        
        initial_response = writer.generate_reply(task)

    if 1:
        task_msg={"role": "user", "content": task}
        writer_msg={"role": "assistant", "content": f'List of topics returned by writer:\n\n{writer.agent_response}\n\n'}
        critic = Critic(data, vars,receiever=writer, verbose=True)
        critic.add_history([task_msg, writer_msg])
        critic_response = critic.reflect_with_llm()

    if 1:
        revision_task = data['agents']['Writer']['revision_task']
        revised_response = writer.generate_reply(revision_task)

    if 1:
        seo_reviewer = Reviewer("SEO Reviewer", data, vars, verbose=True)
        seo_reviewer.add_history([task_msg, writer_msg])
        seo_reviewer_response = seo_reviewer.reflect_with_llm()
    if 1:
        legal_reviewer = Reviewer("Legal Reviewer", data, vars, verbose=True)
        legal_reviewer.add_history([task_msg, writer_msg])
        legal_reviewer_response = legal_reviewer.reflect_with_llm()
    if 1:
        ethics_reviewer = Reviewer("Ethics Reviewer", data, vars, verbose=True)
        ethics_reviewer.add_history([task_msg, writer_msg])
        ethics_reviewer_response = ethics_reviewer.reflect_with_llm()
    if 1:
        seo_msg ={"role": "assistant", "content": f"SEO Reviewer Feedback:\n{seo_reviewer.agent_response}"}
        legal_msg ={"role": "assistant", "content": f"Legal Reviewer Feedback:\n{legal_reviewer.agent_response}"}
        ethics_msg ={"role": "assistant", "content": f"Ethics Reviewer Feedback:\n{ethics_reviewer.agent_response}"}
            
        meta_summarizer = Summarizer("Meta Summarizer", data, vars, verbose=True)
        meta_summarizer.add_history([task_msg, writer_msg, seo_msg, legal_msg, ethics_msg])
        meta_summarizer_response = meta_summarizer.summarize()


    if 1:
        writer.add_history([{"role": "assistant", "content": f'Meta Summarizer Response:\n\n{meta_summarizer_response}'}])
        final_task = revision_task = data['agents']['Writer']['final_task']
        final_response = writer.generate_reply(final_task)
    return final_response


if __name__ == '__main__':
    config=join('config','topics.yaml')
    title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
    generate_topics(title, config)
