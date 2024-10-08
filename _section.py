import yaml, json
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline

# Set verbose to True
apc.verbose = True

if __name__ == '__main__':
    if 0:  # no mock
        py_pipeline_name = 'section'

        yaml_pprompt_config = join('yaml_config', 'section.yaml')
        theme = "DeepLearning.AI"
        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        topic='Introduction: Exploring the DeepLearning.AI Community Ecosystem'
    if 1:  # mock
        py_pipeline_name = 'section'

        yaml_pprompt_config = join('yaml_config', 'section.yaml')
        theme = "DeepLearning.AI"
        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        topic='Introduction: Exploring the DeepLearning.AI Community Ecosystem'
        if 1:
            mock_file = join('mock', 'blog_writer', 'section.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
        
    # Use execute_pipeline
    if 1:
        section = execute_pipeline({'theme':theme, 'title':title, 'topic':topic}, py_pipeline_name, yaml_pprompt_config)
        print(section)
        pp(json.loads(section))

