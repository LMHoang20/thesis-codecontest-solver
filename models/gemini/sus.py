import yaml

with open('models/gemini/test.yaml', 'r') as f:
    content = f.read()
    data = yaml.load(content, Loader=yaml.FullLoader)
    print(data)