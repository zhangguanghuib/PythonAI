# PythonAI

## 1. Create a new branch based on the main branch and make changes in the new branch and then merge the changes from new branch to main branch
```
cd C:\D\Python\PythonAI
git status
git fetch origin
git switch -c guanghui-dev-branch origin/main
git add langgraph\matplotlib
git commit -m "Add matplotlib examples"
git push -u origin guanghui-dev-branch
git switch main
git pull --ff-only origin main
git merge guanghui-dev-branch
git push origin main
```
## 2. Made some change on main branch, synch the code to my dev branch
```
git switch main
git pull --ff-only origin main
git switch guanghui-dev-branch
git merge main
git push -u guanghui-dev-branch
```
