from github import Github
import os
import datetime

token = os.environ["GITHUB_TOKEN"]
g = Github(token)

since_point = datetime.datetime.today() - datetime.timedelta(days=21)
all_commits = []

for repo in g.get_user().get_repos():

    try:
        if True:
        # if (repo.name == 'groot' ) :

            branches = repo.get_branches()
            for b in branches:
                last_modified_branch_str = b.commit.last_modified
                relevant_branch = False
                if last_modified_branch_str == None:
                    relevant_branch = True
                else :
                    last_modified_branch = datetime.datetime.strptime(last_modified_branch_str, '%a, %d %b %Y %H:%M:%S GMT')
                    if last_modified_branch_str > since_point:
                        relevant_branch = True
                if relevant_branch:
                    commits = repo.get_commits(since=since_point, sha = b.commit.sha )
                    for c in commits:
                        all_commits.append( {'repo':repo.name,'branch_name':b.name,'name':c.author.name, 'email':c.author.email, 'login': c.author.login ,'ts':datetime.datetime.strptime(c.last_modified,'%a, %d %b %Y %H:%M:%S GMT').strftime('%d/%m/%Y') } )
    except Exception as error:
        raise error
        print(error)
        print ("Problem with repo:" + str(repo))

for r in all_commits:
    print(r['repo'], '\t',r['branch_name'], '\t',r['name'], '\t',r['login'],'\t',r['email'], '\t',r['ts'])