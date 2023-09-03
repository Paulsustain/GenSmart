#! /bin/sh

# Save Git data
cp -r .git gitold

# Remove all empty Git object files
find .git -type f -empty -delete -print

# Get the current branch name
branchname=$(git branch --show-current)

# Get the latest commit hash
commit=$(tail -2 .git/logs/refs/heads/master | awk '{ print $1 }' | tr -d '[:space:]')

# Set HEAD to this latest commit
git update-ref HEAD $commit

# Pull the latest changes on the current branch (considering remote is origin)
git pull origin $branchname

rm -rf gitold
# echo "If everything looks fine you remove the git backup running :\n\
#       $ rm -rf gitold\n\
# Otherwise restore it with:\n\
#       $ rm -rf .git; mv gitold .git"