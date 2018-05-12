#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

celery -A hack_travel_labs.taskapp worker -l INFO
