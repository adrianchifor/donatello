import hashlib
import hmac
import json
from typing import Dict, List, Union

from github import Github
from github.PullRequest import PullRequest

ALLOWED_ACTIONS = ['created']


class GithubAPI(object):
    def __init__(self, token: str, webhook_secret: str, allowed_repositories: List) -> None:
        """
        Initialise internal Github API object.
        :param token: str
        :param webhook_secret: str
        :param allowed_repositories: List
        """
        self.gh = Github(token)
        self.webhook_secret = bytes(webhook_secret, 'utf-8')
        self.allowed_repositories = allowed_repositories

    def webhook(self, request: Dict, signature: str) -> Union[Dict, None]:
        """
        Parse Github webhook request.
        :param request: Dict
        :param signature: str
        :return: event: Dict or None
        """
        if not request:
            print("Empty request.")
            return None

        if not signature:
            print("No 'X-Hub-Signature' header found.")
            return None

        repo_name = request['repository']['full_name']

        if repo_name not in self.allowed_repositories:
            print(f"Repository not allowed: {repo_name}.")
            return None

        action = request['action']

        if action not in ALLOWED_ACTIONS:
            print(f"Action not allowed: {action}.")
            return None

        event = {
            "action": action,
            "pr_number": request['issue']['number'],
            "author": request['comment']['user']['login'],
            "repo_name": repo_name,
            "body": request['comment']['body'],
        }

        return event

    def _verify_signature(self, msg: Dict, signature: str) -> bool:
        """
        Verify HMAC signature of the payload.
        :param msg: Dict
        :param signature
        :return: bool
        """
        sha, signature_mac = signature.split('=')

        if sha != 'sha1':
            return False

        message = bytes(json.dumps(msg), 'utf-8')
        hash = hmac.new(self.webhook_secret, message, digestmod=hashlib.sha1)

        return hmac.compare_digest(str(hash.hexdigest()), signature_mac)

    def _get_pull_request(self, repository: str, pr_number: int) -> PullRequest:
        """
        Return Pull Request object.
        :param repository: str
        :param pr_number: int
        :return: pr: github.PullRequest.PullRequest
        """
        repo = self.gh.get_repo(repository)
        pr = repo.get_pull(int(pr_number))

        return pr

    def is_author(self, repository: str, pr_number: int, user: str) -> bool:
        """
        Return True if user is the author of the PR.
        :param repository: str
        :param pr_number: int
        :param user: str
        :return: bool
        """
        pr = self._get_pull_request(repository, pr_number)
        author = pr.user.login

        return author == user

    def is_collaborator(self, repository: str, user: str) -> bool:
        """
        Return True if user is the collaborator of the PR.
        :param repository: str
        :param user: str
        :return: bool
        """
        repo = self.gh.get_repo(repository)
        collaborators = [collaborator.login for collaborator in repo.get_collaborators()]

        return user in collaborators

    def get_comments(self, repository: str, pr_number: int) -> List:
        """
        Return Github comments on a PR.
        :param repository: str
        :param pr_number: int
        :return comments: List
        """
        pr = self._get_pull_request(repository, pr_number)
        review_comments = pr.get_issue_comments()
        comments = [{"body": comment.body, "user": comment.user.login} for comment in review_comments]

        return comments

    def comment(self, repository: str, pr_number: int, body: str) -> bool:
        """
        Comment on Github PR.
        :param repository: str
        :param pr_number: int
        :param body: str
        :return bool
        """
        comments = self.get_comments(repository, pr_number)
        pr = self._get_pull_request(repository, pr_number)

        for comment in comments:
            if body == comment["body"]:
                print("Comment already posted.")
                return False

        pr.create_issue_comment(body)

        return True
