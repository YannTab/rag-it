
import json
import parser

def feed(filename:str):
    with open(filename) as file:
        file_content = json.load(file)
    #n_commments = len(file_content)

    for i,content in enumerate(file_content[11:]):
        title = content['title']
        print(f'parsing content {i} ...: Title:{title}')
        parser.parser(content)
        

