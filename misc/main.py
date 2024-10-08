
import yaml, json
from    os.path import join, isfile
from   pprint import pprint as pp   

import  include.config.init_config as  init_config

init_config.init(**{})
apc = init_config.apc

apc.verbose = True

from include.utils import execute_pipeline


if __name__ == '__main__':
    if 0: #no mock
        py_pipeline_name='blog_writer'

        yaml_pprompt_config=join('config','topics.yaml')

        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
    if 1: #mock
        py_pipeline_name='mock_blog_writer'

        yaml_pprompt_config=join('config','topics.yaml')

        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        if 1:
            mock_file=join('mock','blog_writer','blog_writer_topics.json')
            assert isfile(mock_file), f"Mock file not found: {mock_file}"
            apc.load_mock(mock_file) 
    topics= execute_pipeline(title, py_pipeline_name, yaml_pprompt_config)
    print(topics)
    pp(json.loads(topics))
