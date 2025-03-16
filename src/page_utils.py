import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines: list[str] = markdown.split("\n")
    header = list(filter(lambda line: line.startswith("# "), lines))
    if header == []:
        raise Exception("no h1 present")
    return header[0][2:].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    markdown = f.read()
    f.close()
    t = open(template_path)
    template = t.read()
    t.close()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(content)
    f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # TODO is no good yet
    # crawl every entry in content dir
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        for item in os.listdir(dir_path_content):
            current_level_path = f"{dir_path_content}/{item}"
            current_level_dest = f"{dest_dir_path}/{item}"
            print('item', item, 'at', current_level_path, 'going to', current_level_dest)
            if os.path.isfile(item):
                generate_page(current_level_path, template_path, current_level_dest)
            else:
                generate_pages_recursive(current_level_path, template_path, current_level_dest)
            return
    # for each md file found, generate .html using template.html
    # write each gen. page to public directory using same structure
    