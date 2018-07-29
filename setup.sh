#!/usr/bin/env sh

set -eo pipefail

function install
{
    install_global_deps
    install_local_deps
    setup_virtualenv
}

function setup_virtualenv
{
    virtualenv venv
}

function install_global_deps
{
    sudo pip install virtualenv
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
