import yaml, json
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline

# Set verbose to True
apc.verbose = True

if __name__ == '__main__':
    if 1:  # mock
        py_pipeline_name = 'mock_blog_writer'

        yaml_pprompt_config = join('yaml_config', 'topics.yaml')

        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        if 1:
            mock_file = join('mock', 'blog_writer', 'blog_writer_topics.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
        
    # Use execute_pipeline
    if 1:
        topics = execute_pipeline(title, py_pipeline_name, yaml_pprompt_config)
        print(topics)
        pp(json.loads(topics))
