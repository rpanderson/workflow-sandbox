import subprocess
import tempfile
from pathlib import Path

WORKFLOW_SRC = Path('../.github/workflows/release.yml').read_text(encoding='utf8')
HEAD = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

def deploy(repo_slug, mainbranch='master', commit_to_mainbranch=False):
    """Deploy latest workflow to a repo:
    * Clone given repo to a temporary directory
    * Checkout the main branch
    * if commit_to_mainbranch is False, create a new branch called
      <mainbranch>-workflow-sandbox-<hash> where <hash> is the current commit hash of
      HEAD in the workflow-sandbox repo
    * Copy release.yml from workflow-sandbox to the repo
    * Add it
    * Commit
    * Push
    * if commit_to_mainbranch is False, return a URL for creating a pull request, else
      return None
    """
    github_user, project_name = repo_slug.split('/')
    url = f"ssh://git@github.com/{github_user}/{project_name}"
    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.check_call(['git', 'clone', url], cwd=tempdir)
        repo = Path(tempdir) / project_name
        workflow_path = Path(repo) / '.github' / 'workflows' / 'release.yml'
        workflow_config_path = Path(repo) / '.github' / 'workflows' / 'release-vars.sh'
        if not workflow_config_path.exists() or not workflow_path.exists():
            msg = f"{repo_slug} does not appear to be using a workflow-sandbox workflow"
            raise RuntimeError(msg)
        subprocess.check_call(['git', 'switch', mainbranch], cwd=repo)
        if not commit_to_mainbranch:
            newbranch = f"{mainbranch}-workflow-sandbox-{HEAD}"
            subprocess.check_call(['git', 'switch', '-c', newbranch], cwd=repo)
        workflow_path.write_text(WORKFLOW_SRC, encoding='utf8')
        subprocess.check_call(['git', 'add', workflow_path], cwd=repo)
        status = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo)
        if status.returncode == 0:
            print(f"{repo_slug} workflow is already up to date")
            return
        commit_msg = f"sync workflow with rpanderson/workflow-sandbox@{HEAD}"
        subprocess.check_call(['git', 'commit', '-m', commit_msg], cwd=repo)
        if commit_to_mainbranch:
            subprocess.check_call(['git', 'push'], cwd=repo)
        else:
            subprocess.check_call(['git', 'push', '-u', 'origin', newbranch], cwd=repo)
            return f"https://github.com/{repo_slug}/compare/{mainbranch}...{newbranch}?expand=1"

if __name__ == '__main__':

    # If true, workflows updated directly in main branch and pushed. Otherwise, a new
    # branch is created and pushed.
    COMMIT_TO_MAINBRANCH = False

    REPOS = [
        'labscript-suite/labscript',
        'labscript-suite/runmanager',
        'labscript-suite/runviewer',
        'labscript-suite/blacs',
        'labscript-suite/lyse',
        'labscript-suite/labscript-utils',
        'labscript-suite/labscript-suite',
        'labscript-suite/labscript-devices',
        'labscript-suite/labscript-c-extensions',
        'chrisjbillington/zprocess',
        'chrisjbillington/desktop-app',
        'philipstarkey/qtutils',
    ]

    # Other projects that don't use the workflow verbatim but use some aspects of it
    # that may need to be updated manually. Included here as a checklist
    #
    # chrisjbillington/setuptools-conda
    # chrisjbillington/ci-helper
    # labscript-suite/vendored-conda-builds

    pr_urls = []
    for repo in REPOS:
        url = deploy(repo, commit_to_mainbranch=COMMIT_TO_MAINBRANCH)
        if url is not None:
            pr_urls.append(url)

    # Print a URL for each repo to create a pull request with the newly-created branch
    print("URLs to create PRs:")
    for url in pr_urls:
        print(url)
