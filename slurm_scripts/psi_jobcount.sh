#!/bin/bash
# Depths: [0] angles [1] theory [2] angle#
# modify "! -path" to control which paths to avoid

cd /DFS-B/DATA/mobley/limvt/3_neutral/dihed_psi4

ALL_JOBS=$(find ./ -mindepth 2 -type d)
ALL_JOBS_ARRAY=($ALL_JOBS)

REM_JOBS=$(find ./ -mindepth 2 -type d '!' -exec test -e "{}/timer.dat" ';' -print)
REM_JOBS_ARRAY=($REM_JOBS)

printf "\n\nTOTAL DIRECTORY SIZE: ${#ALL_JOBS_ARRAY[@]}"
printf "\nTOTAL NUMBER OF JOBS FOUND: ${#REM_JOBS_ARRAY[@]}\n\n"

# print list of remaining jobs
echo ${REM_JOBS_ARRAY[@]}
