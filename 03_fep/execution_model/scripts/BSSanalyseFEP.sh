#!/usr/bin/env bash
echo $SLURM_JOB_NAME
date
$BSSHOME/sire.app/bin/python scripts/BSSanalyseFEP.py $1 $2
sleep 5
exit 0
