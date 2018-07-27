#!/usr/bin/env sh

set -eo pipefail

function test
{
    source venv/bin/activate
    pytest
    deactivate
}

"$@"