import yaml, json
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline

# Set verbose to True
apc.verbose = True

if __name__ == '__main__':
    if 0:  # no mock
        py_pipeline_name = 'titles'

        yaml_pprompt_config = join('yaml_config', 'titles.yaml')

        theme = "DeepLearning.AI"

    if 1:  # mock
        py_pipeline_name = 'titles'

        yaml_pprompt_config = join('yaml_config', 'titles.yaml')

        theme = "DeepLearning.AI"
        if 1:
            mock_file = join('mock', 'blog_writer', 'titles.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
        
    # Use execute_pipeline
    if 1:
        titles = execute_pipeline({'theme':theme}, py_pipeline_name, yaml_pprompt_config)
        print(titles)
        pp(json.loads(titles))

