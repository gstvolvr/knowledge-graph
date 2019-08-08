#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/../conf/env.sh

## path to gist repo
path=${1}

git --git-dir=$path/.git --work-tree=$path status
git --git-dir=$path/.git --work-tree=$path add knowledge_graph.csv
git --git-dir=$path/.git --work-tree=$path commit --allow-empty-message -m ''
git --git-dir=$path/.git --work-tree=$path push origin master
