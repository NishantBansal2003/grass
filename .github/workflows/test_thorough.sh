#!/usr/bin/env bash

# fail on non-zero return code from a subprocess
set -e

grass --tmp-project XY --exec \
    python3 -m grass.gunittest.main \
    --grassdata $HOME --location nc_spm_full_v2alpha2 --location-type nc \
    --min-success 100 $@
