import yaml, json, click
from os.path import join, isfile
from pprint import pprint as pp

# Import apc and execute_pipeline from auto_reflection
from auto_reflection import apc, execute_pipeline


# Set verbose to True
apc.verbose = True
# auto_reflection/main.py
@click.command()
@click.option('--theme', default="DeepLearning.AI", help='Theme for the pipeline')
@click.option('--title', default="Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI", help='Title for the pipeline')
@click.option('--topic', default='Introduction: Exploring the DeepLearning.AI Community Ecosystem', help='Topic for the pipeline')
@click.option('--py_pipeline_name', default="mocked_section", help='Python pipeline name')
@click.option('--yaml_pprompt_config', default='section.yaml', help='YAML config file')
def main(theme, title, topic, py_pipeline_name, yaml_pprompt_config):
    if 1:  # mock
        

        yaml_pprompt_config_fn = join('yaml_config', yaml_pprompt_config)

        
        if 1:
            mock_file = join('mock', 'blog_writer', 'section.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
    
    apc.theme, apc.title,apc.topic, apc.py_pipeline_name, apc.yaml_pprompt_config =theme,  title,topic, py_pipeline_name, yaml_pprompt_config_fn  
    section = execute_pipeline({'theme':theme, 'title':title, 'topic':topic}, apc.py_pipeline_name, apc.yaml_pprompt_config)
    pp(json.loads(section))

#pip install -e .
#python setup.py sdist bdist_wheel
#twine upload dist/*


if __name__ == '__main__':
    main()