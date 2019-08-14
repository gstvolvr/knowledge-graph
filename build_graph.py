import configparser
import datetime
import os
import re

def clean_name(name):
    """clean up ipynb file names"""

    name = name.replace(".ipynb", "")

    if not '_' in name and not '-' in name:
        return name.lower()

    return " ".join([word for word in name.replace('-', '_').replace(' ', '_').split('_')]).lower()

def clean_path(path):
    return "/".join(path.split("/")[5:])

def graph(dir_path, graph_path):
    """iterate over files and find links"""

    def recurse(parent_path, res=[], depth=0):

        for entry in os.scandir(parent_path):

            if entry.is_file() and entry.name[0] != ".":
                with open(entry.path, "r") as f:
                    text = f.read()
                    matches = re.findall("\[([^\]]{4,30})\]\(([^)]+ipynb[^)]*)\)", text)
                    category = os.path.basename(parent_path)

                    res.append(",".join(["file", str(depth), clean_name(category), clean_path(entry.path), clean_name(entry.name), clean_path(entry.path)]) + "\n")

                    for name, link in matches:
                        parent_dir = os.path.join(entry.path, os.pardir)
                        other_path = os.path.join(parent_path, link)
                        file_name = clean_name(other_path.split("/")[-1].split("#")[0])

                        res.append(",".join(["notebook", str(depth), clean_name(entry.name), clean_path(entry.path), clean_name(file_name), clean_path(other_path)]) + "\n")
            elif entry.name[0] != ".":
                parent_path = os.path.abspath(os.path.join(entry, os.path.pardir))
                parent_name = parent_path.split("/")[-1]

                # make link between parent and sub directories
                if parent_name != "concepts":
                    res.append(",".join(["dir", str(depth), clean_name(parent_path.split("/")[-1]), clean_path(parent_path), clean_name(entry.name), clean_path(entry.path)]) + "\n")
                recurse(entry.path, res, depth+1)
        return res

    with open(graph_path, "w") as w:
        w.write("type,depth,from,from_path,to,to_path,to_path\n")
        lines = recurse(dir_path)
        w.writelines(lines)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    graph(config["graph"]["notebooks_repo"], config["graph"]["output_path"])
