#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

celery -A hack_travel_labs.taskapp beat -l INFO
