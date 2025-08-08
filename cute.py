#! python3
from xcute import cute, LiveReload

cute(
    pkg_name = 'pip_outdated',
    lint = 'pylint cute.py tests {pkg_name}',
    test = ["lint", 'readme_build', "pytest --cov={pkg_name}"],
    bump_pre = 'test',
    bump_post = ['dist', 'release', 'publish', 'install'],
    # https://stackoverflow.com/q/26545668/3413125
    clean = 'x-clean build dist *.egg-info',
    dist_pre = 'clean',
    dist = 'python -m build',
    release = [
        'git add .',
        'git commit -m "Release v{version}"',
        'git tag -a v{version} -m "Release v{version}"'
    ],
    publish = [
        'twine upload dist/*',
        'git push --follow-tags'
    ],
    install = 'pip install -e .',
    readme_build = [
        ('rst2html5 --no-raw --exit-status=1 --verbose '
         'README.rst | x-pipe build/README.html')
    ],
    readme_pre = "readme_build",
    readme = LiveReload("README.rst", "readme_build", "build/README.html")
)
