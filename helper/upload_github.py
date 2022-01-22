import os

from future.moves import pickle
from github import Github

from helper import cfg

def upload_github(file_path):

    g = Github(cfg['github_token'])
    repo = g.get_repo("jinyiabc/china_stock_data")
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    with open(file_path, 'rb') as file:
        content = file.read()
        # file.seek(0)
        # content = pickle.load(file)

    # Upload to github
    git_prefix = 'module-03/'
    head, tail = os.path.split(file_path)
    git_file = git_prefix + tail
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')
