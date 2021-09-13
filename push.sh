#!/bin/bash
shopt -s expand_aliases
source ~/.bash_aliases
source ~/.bash_profile

# Make changes to code before running
egg='nemesis_scan'
if [[ "$egg" == "" ]]; then
	echo "WARNING: Edit this file to include your package"
	exit
fi
pip_egg="src/""$egg"".egg-info"

cat .gitignore | while read tempfile
do
	rm $tempfile -r 1>/dev/null 2>/dev/null
done

{ python3 up_version.py || exit; } && vim -O CHANGELOG.md <(git log)
python3 setup.py sdist
twine upload dist/* && rm $pip_egg build/ dist/ -r 1>/dev/null 2>/dev/null
git add .
git commit -m "Bump $egg to new version"
git push -u origin master
