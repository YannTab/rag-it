# Define the logic for the parser function

## The parser should take JSON object as an entry and make calls to the LLM api by providing context and data
## The parser will then call the printer module with the expected data (id, date, comment, score, sentiment)

from collections import deque
import json

import query
import printer

def parser(post:dict):
    """
    """
    visited = []
    if query.call_filter_api(title=post['title'], body=post['body']) == 'no':
        pass
    else:
        comment_stack = deque([(post, [post])])
        while comment_stack:
            ## visiting a node
            comment_node, path = comment_stack.pop()
            if 'comments' in comment_node.keys():
                comment_node['replies'] = comment_node['comments']
            if comment_node['replies']:
                for reply in comment_node['replies']:
                    comment_stack.append((reply, path + [reply]))
            else:
                ## No replies == leaf
                ## if leaf call LLM 
                visited = formatter(post['title'], path, visited_nodes=visited)

def formatter(title:str, comment_list:list[dict], visited_nodes:list):
    
    n = len(comment_list)
    reverse_comment_list = list(reversed(comment_list))
    lis_to_print = []
    for i,comment in enumerate(reverse_comment_list):
        if comment['id'] not in visited_nodes:
            context = []
            for j in range(i+1,n,1):
                # Build the context of the comment
                context.append(reverse_comment_list[j]['body']) ## comment n-1, n-2, ..., 0
            context.append(title)
                
            ## Get attributes of the focal comment
            id = comment['id']
            body = comment['body']
            date = comment['created']
            score = comment['score']

            ### make the llm call
            response = query.call_sentiment_api(comment==body, context=context)
            print(f"\tparsing comment {id} ...")

            ### Updating visited nodes
            visited_nodes = visited_nodes.copy()
            visited_nodes.append(comment['id'])

            ### call the printer function
            lis_to_print.append(
                {'id':id,
                'date':date,
                'score':score,
                'sentiment':response}
            )
    printer.printer(lis_to_print, filename="output_1.csv")
    return visited_nodes

# if __name__ == "__main__":
#     parser(file_content[3])