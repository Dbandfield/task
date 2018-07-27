#!/usr/bin/env sh

set -eo pipefail

function setup_virtualenv
{
    virtualenv venv
}

function install_global_deps
{
    sudo pip install virtualenv
    setup_virtualenv()
}

function install_local_deps
{
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
}

function test
{
    source venv/bin/activate
    pytest
    deactivate
}

"$@"
