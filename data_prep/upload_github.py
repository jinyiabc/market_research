import io

from github import Github
from helper.configSQL import cfg

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



with open('../resource/300072.csv', 'r') as file:
    content = file.read()

# Upload to github
git_prefix = 'module-03/'
git_file = git_prefix + '300072.csv'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="main")
    print(git_file + ' CREATED')





# Create zip file.
from zipfile import ZipFile, ZipInfo

# archive = io.BytesIO()
# with ZipFile(archive, 'w') as zipObj:
# # zipObj = ZipFile('sample.zip', 'w')
#     with open('../300072.csv', 'r') as file:
#         zip_file = ZipInfo("sample.zip")
#         zipObj.writestr(zip_file, file.read())

# #create a ZipFile object
# zipObj = ZipFile('sample.zip', 'w')
# # Add multiple files to the zip
# zipObj.write('../300072.csv')
# # close the Zip File
# zipObj.close()
# with ZipFile('sample.zip') as myzip:
#     content = myzip