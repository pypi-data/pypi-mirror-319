from os.path import join


def grep(search_string, path):
    output = ''
    
    with open(join(path)) as f:
        for i in f:
            if search_string in i:
                output += i
    
    return output
