
def get_content(path):
    with open(path) as f:
        return f.read()

def set_content_append(path, content):
    with open(path, 'a') as file: 
        # Write the new content 
        file.write(content)

def set_content(path, content):
    with open(path, 'w') as file: 
        # Write the new content 
        file.write(content)

