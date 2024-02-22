import gitlab
import sys
sys.path.insert(0, '..')
from static.constants import names, url, private_token, project_name, member_info

def get_gitlab_info():
    if not url or not private_token or not project_name:
        raise ValueError("Missing required arguments: url, private_token, and project_name.")

    gl = gitlab.Gitlab(url, private_token)
    try:
        project = gl.projects.get(project_name, statistics=True)
        total_commit_count = project.statistics['commit_count']

        user_commit_info = {}
        for page in range(1, (total_commit_count // 100) + 2):
            commits = project.commits.list(all=True, page=page, per_page=100)
            for commit in commits:
                committer = commit.committer_name
                if committer in user_commit_info:
                    user_commit_info[committer] += 1
                else:
                    user_commit_info[committer] = 1
            if not commits:
                break

        # print(project.issues.list(all=True)[0].author['name'])
        total_issue_count = 0
        issue_info = {}
        for page in range(1, (total_issue_count // 100) + 2):
            issues = project.issues.list(all=True, page=page, per_page=100)
            for issue in issues:
                issuer = issue.author['username']
                if issuer in issue_info:
                    issue_info[issuer] += 1
                else:
                    issue_info[issuer] = 1
            if not issues:
                break
            total_issue_count += len(issues)

        all_info = {
            "total_commit_count": total_commit_count,
            "user_commit_info": user_commit_info,
            "total_issue_count": total_issue_count,
            "issue_info": issue_info}

        return all_info  # success
    except gitlab.exceptions.GitlabHttpError as e:
        raise gitlab.exceptions.GitlabHttpError(e.status_code, e.message) from e


def find_user(d, k):
    # helper method of user_gitlab_info()
    for key, values in d.items():
        if k in values:
            return key
    return None


def sort_by_total(d):
    # helper function for user_all_info()
    sorted_dict = dict(sorted(d.items(), key=lambda x: x[1]['commits'] + x[1]['issues'], reverse=False))
    return sorted_dict


def user_gitlab_info(all_info):
    # this is a helper function for user_all_info()
    info_by_user = {key: {"commits": 0, "issues": 0} for key in names}
    # commits
    user_commit_info = all_info['user_commit_info']
    for key in user_commit_info:
        user = find_user(names, key)
        commit_cnt = user_commit_info[key]
        info_by_user[user]["commits"] += commit_cnt
    # issues
    user_issue_info = all_info['issue_info']
    for key in user_issue_info:
        user = find_user(names, key)
        issue_cnt = user_issue_info[key]
        info_by_user[user]["issues"] += issue_cnt

    return info_by_user


def group_gitlab_info(all_info):
    return {"commits":all_info['total_commit_count'], "issues":all_info['total_issue_count']}


def user_all_info(all_info):
    gitlab_stats = user_gitlab_info(all_info)
    for name, value in gitlab_stats.items():
        if name in member_info:
            member_info[name].update(value)
        else:
            member_info[name] = value  # Add the key-value pair to combined_dict if it doesn't exist
    sorted_info = sort_by_total(member_info)
    return sorted_info


def main():
    try:
        all_info = get_gitlab_info()

        print(
            f"-----------------------\nTotal commits in project '{project_name}': {all_info['total_commit_count']}\n-----------------------")

        if all_info['total_commit_count'] > 0:
            print("Individual commits:")
            user_commit_info = all_info['user_commit_info']
            for key in user_commit_info:
                print(f"'{key}' committed {user_commit_info[key]} time(s)")

        print(
            f"-----------------------\nTotal issues raised in project '{project_name}': {all_info['total_issue_count']}\n-----------------------")

        if all_info['total_issue_count'] > 0:
            print("Individual issues:")
            issue_info = all_info['issue_info']
            for key in issue_info:
                print(f"'{key}' raised {issue_info[key]} issue(s)")
            print('-----------------------')

        sorted_info = user_all_info(all_info)
        for user in sorted_info:
            print(f"{user}: {sorted_info[user]}")
    except ValueError as e:
        print(f"Error: {e}")
    except gitlab.exceptions.GitlabHttpError as e:
        print(f"API error: {e}")


if __name__ == "__main__":
    main()
