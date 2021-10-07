backend_image_repo="621544995223.dkr.ecr.us-west-2.amazonaws.com/budget-tracker-ecr-backend"

if [[ -z $1 ]]; then
    printf "ERROR: Please provide a commit message. \n"
    exit 1
fi

commit_message="$1"
printf "commit_message: $commit_message \n"
git add -u
printf "About to commit...\n"
git commit -m "$commit_message"
printf "About to push to git...\n"
git push origin

printf "About to do docker stuff...\n"
backend_latest_version=$(cat version.txt)
backend_latest_image_tag="$backend_image_repo:$backend_latest_version"
docker push $backend_latest_image_tag
