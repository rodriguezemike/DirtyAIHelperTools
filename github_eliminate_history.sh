cp * ../
git checkout --orphan new_branch
git branch
git add -A
git commit -am "Commit"
git branch -D main
git status
git branch -m main
git push -f origin main
