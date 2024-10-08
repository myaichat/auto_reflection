import yaml, json, click
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline


# Set verbose to True
apc.verbose = True
# auto_reflection/main.py
@click.command()
@click.option('--title', default="Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI", help='Title for the pipeline')
@click.option('--py_pipeline_name', default="mocked_topics", help='Python pipeline name')
@click.option('--yaml_pprompt_config', default='topics.yaml', help='YAML config file')
def main(title, py_pipeline_name, yaml_pprompt_config):
    if 1:  # mock
        #py_pipeline_name = 'mocked_topics'

        yaml_pprompt_config_fn = join('yaml_config', yaml_pprompt_config)

        
        if 1:
            mock_file = join('mock', 'blog_writer', 'topics.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
    print(title, py_pipeline_name, yaml_pprompt_config_fn)
    apc.title, apc.py_pipeline_name, apc.yaml_pprompt_config = title, py_pipeline_name, yaml_pprompt_config_fn  
    topics = execute_pipeline({'title':apc.title}, apc.py_pipeline_name, apc.yaml_pprompt_config)
    pp(json.loads(topics))

#pip install -e .
#python setup.py sdist bdist_wheel
#twine upload dist/*


if __name__ == '__main__':
    main()