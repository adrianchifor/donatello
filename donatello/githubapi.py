from github import Github

ALLOWED_ACTIONS = ['created']


class GithubAPI(object):
    def __init__(self, token, webhook_secret):
        self.gh = Github(token)
        self.webhook_secret = webhook_secret

    def webhook(self, request):
        """
        Parse Github webhook request.
        :param request: dict
        """
        if not request:
            print("Empty request.")
            return None

        action = request['action']

        if action not in ALLOWED_ACTIONS:
            print(f"Action not allowed: {action}.")
            return None

        event = {
            "action": action,
            "pr_number": request['issue']['number'],
            "author": request['comment']['user']['login'],
            "repo_name": request['repository']['full_name'],
            "body": request['comment']['body'],
        }

        return event

    def _get_pull_request(self, repository, pr_number):
        repo = self.gh.get_repo(repository)
        pr = repo.get_pull(int(pr_number))

        return pr

    def get_comments(self, repository, pr_number):
        """
        Return Github comments on a PR.
        :param repository: str
        :param pr_number: init
        """
        pr = self._get_pull_request(repository, pr_number)
        review_comments = pr.get_issue_comments()
        comments = [{"body": comment.body, "user": comment.user.login} for comment in review_comments]

        return comments

    def comment(self, repository, pr_number, body):
        """
        Comment on Github PR.
        :param repository: str
        :param pr_number: init
        :param body: str
        """
        comments = self.get_comments(repository, pr_number)
        pr = self._get_pull_request(repository, pr_number)

        for comment in comments:
            if body == comment.body:
                print("Comment already posted.")
                return False

        pr.create_issue_comment(body)

        return True

