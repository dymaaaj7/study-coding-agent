# Contributing instructions

Contributors to this repository must follow the instructions from this file.

## Initial install

Steps in this section should be executed only when cloning the repository for
the first time.

### Cloning the repository

The first step is to clone the repository. To be able to clone, you need to
create/prepare your SSH key (for help check [this]
(https://docs.github.com/en/authentication/connecting-to-github-with-ssh)).

```console
mkdir -p ~/source/study-coding-agent

Then `cd` into it:

```console
cd ~/source/study-coding-agent
```

and clone the repository:

```console
git clone git@github.com:dymaaaj7/study-coding-agent.git
```

If you haven't already created global `git` configuration about yourself, you
should do it now. To create global configuration, execute:

```console
git config --global user.name "Your Name"
git config --global user.email "your.email@dd.dev"
```

Alternatively, you can make this configuration locally, only for the newly
cloned repository:

```console
cd ~/source/study-coding-agent
git config --local user.name "Your Name"
git config --local user.email "your.email@dd.dev"
```

### Creating the virtual environment

To create Python virtual environment, you first need to ensure that you have
necessary packages installed on your system:

```console
sudo apt update
sudo apt install python3-virtualenv
```

Then create the virtual environment and activate it:

```console
cd ~/source/
python3 -m venv venv
source venv/bin/activate
```

Next step is to install the project locally by executing:

```console
pip install -e .[dev,test]
```

Finally, you should install `pre-commit` by executing:

```console
pre-commit install
pre-commit install-hooks
```

## Start working

When you start working on the project, the first thing is to ensure that you
have the latest version of `main` branch:

```console
git pull --all
git fetch --all
```

Additionally, if you still haven't installed the project, or if `pyproject.toml`
file is changed meanwhile, you should:

```console
pip install -e .[dev,test]
```

