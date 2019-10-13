from pip_outdated.find_require import parse_cfg

def test_parse_cfg(tmp_path):
    file = tmp_path / "setup.cfg"
    file.write_text("""
[options]
setup_requires =
    setuptools_scm >= 1.15.0
    setuptools_scm_git_archive >= 1.0
    
install_requires =
    ansible >= 2.5
    ansible-lint >= 4.0.2, < 5
    
[options.extras_require]
docs =
    alabaster
    Sphinx""")
    
    names = [r.project_name for r in parse_cfg(str(file))]
    assert names == [
        "setuptools-scm",
        "setuptools-scm-git-archive",
        "ansible",
        "ansible-lint",
        "alabaster",
        "Sphinx"
    ]
    