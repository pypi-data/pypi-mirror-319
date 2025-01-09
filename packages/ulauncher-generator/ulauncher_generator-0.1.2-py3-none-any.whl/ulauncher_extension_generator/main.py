#!/usr/bin/env python
""" Ulauncher extension generator """

import json
import keyword
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'


def generate_versions():
    versions = {
        "versions": [  {"required_api_version": "2", "commit": "master"} ]
    }
    return json.dumps(versions, indent=4)

def generate_manifest(name, description, developer_name, homepage_url, keyword):
    manifest = {
        "required_api_version": "2.0.0",
        "name": name,
        "description": description,
        "developer_name": developer_name,
        "homepage_url": homepage_url,
        "icon": "images/icon.png",
        "options": {
            "query_debounce": 0.1
        },
        "preferences": [
            {
                "id": f"{keyword}_kw",
                "type": "keyword",
                "name": name,
                "description": description,
                "default_value": keyword,
            }
        ]
    }
    return json.dumps(manifest, indent=4)

def generate_main_py(extension_name):
    main_py_content = f'''
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

class {extension_name}(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='{extension_name}',
                                         description='{extension_name} description',
                                         on_enter=HideWindowAction()))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='{extension_name}',
                                         description='{extension_name} description',
                                         on_enter=HideWindowAction()))

        return RenderResultListAction(items)


if __name__ == '__main__':
    {extension_name}().run()

'''
    return main_py_content

def generate_requirements_txt():
    return ""

def main():
    extension_name = input(f"{BLUE}Enter the name of your extension: {RESET}")
    description = input(f"{GREEN}Enter a description for your extension: {RESET}")
    developer_name = input(f"{BOLD}Enter your name (developer name): {RESET}")
    homepage_url = input(f"{RED}Enter the homepage URL for your extension: {RESET}")
    keyword = input(f"{BLUE}Enter keyword trigger for your extension e.g dm: {RESET}" )

    manifest_content = generate_manifest(extension_name, description, developer_name, homepage_url, keyword)
    main_py_content = generate_main_py(extension_name.replace(" ", "").replace("-", ""))
    requirements_txt_content = generate_requirements_txt()

    extension_dir = extension_name.replace(" ", "").replace("-", "")
    os.makedirs(extension_dir, exist_ok=True)
    os.makedirs(os.path.join(extension_dir, "images"), exist_ok=True)
    versions_content = generate_versions()
    with open(os.path.join(extension_dir, "versions.json"), "w") as f:
        f.write(versions_content)
    with open(os.path.join(extension_dir, "manifest.json"), "w") as f:
        f.write(manifest_content)
    with open(os.path.join(extension_dir, "main.py"), "w") as f:
        f.write(main_py_content)
    with open(os.path.join(extension_dir, "requirements.txt"), "w") as f:
        f.write(requirements_txt_content)

    print(f"\nSuccessfully created Ulauncher extension boilerplate for '{extension_name}'.")
    print(f"You can find the generated files in the '{extension_dir}' directory.")

if __name__ == "__main__":
    main()
