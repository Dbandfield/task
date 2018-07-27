#!/usr/bin/env sh

set -eo pipefail

function global_install
{
    pip install virtualenv
    virtualenv venv
}

function local_install
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