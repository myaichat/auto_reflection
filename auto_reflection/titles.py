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
@click.option('--py_pipeline_name', default="mocked_titles", help='Python pipeline name')
@click.option('--yaml_pprompt_config', default='titles.yaml', help='YAML config file')
def main(theme, py_pipeline_name, yaml_pprompt_config):
    if 1:  # mock
        #py_pipeline_name = 'mocked_topics'

        yaml_pprompt_config_fn = join('yaml_config', yaml_pprompt_config)

        
        if 1:
            mock_file = join('mock', 'blog_writer', 'titles.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file)  # Access apc to load mock data
    print(theme, py_pipeline_name, yaml_pprompt_config_fn)
    apc.theme, apc.py_pipeline_name, apc.yaml_pprompt_config = theme, py_pipeline_name, yaml_pprompt_config_fn  
    titles = execute_pipeline({'theme': apc.theme}, apc.py_pipeline_name, apc.yaml_pprompt_config)
    pp(json.loads(titles))

#pip install -e .
#python setup.py sdist bdist_wheel
#twine upload dist/*


if __name__ == '__main__':
    main()