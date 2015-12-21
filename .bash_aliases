alias drmi='docker rmi $(docker images | grep "^<none>" | awk '"'"'{print $3}'"'"') '
alias drmc='docker rm $(docker ps -aq)'
alias dkill='docker kill $(docker ps -aq)'
alias dweb='docker exec -ti webserver bash'
alias ddao='docker exec -ti daoserver bash'

alias behat-commands='docker run -it --rm behat_image behat -dl'

mcd () {
    mkdir -p $1
    cd $1
}
