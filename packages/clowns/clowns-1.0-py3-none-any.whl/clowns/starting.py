import importlib.resources as pkg_resources

teor = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4"
}

content = ''


def write(name):
    global content

    resource_package = 'clowns.t'

    keys = [key for key, val in teor.items() if val == name]

    resource_path = f'{keys[0]}.txt'
    with pkg_resources.open_text(resource_package, resource_path) as file:
        content = file.read()
    return content
