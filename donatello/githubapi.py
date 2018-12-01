from github import Github


class GithubAPI(object):
    def __init__(self, token, webhook_secret):
        self.gh = Github(token)
        self.webhook_secret = webhook_secret

    def webhook(self, request):
        """
        Parse Github webhook request.
        :param request: dict
        """
        print(f"Request: {request}")

    def comment(self, repository, pr_number, body):
        """
        Comment on Github PR.
        :param repository: str
        :param pr_number: init
        :param body: str
        """
        repo = self.gh.get_repo(repository)
        pr = repo.get_pull(int(pr_number))
        review_comments = pr.get_review_comments()

        comments = [comment.body for comment in review_comments]

        if body in comments:
            print("Comment already posted.")
            return False

        pr.create_issue_comment(body)

        return True

