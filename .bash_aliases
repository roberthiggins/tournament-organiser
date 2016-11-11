alias drmi='docker rmi -f $(docker images -q -a -f dangling=true)'
alias drmc='docker rm $(docker ps -aq)'
alias dkill='docker kill $(docker ps -aq)'
alias dvkill='docker volume rm $(docker volume ls -qf dangling=true)'
alias dweb='docker exec -ti webserver bash'
alias ddao='docker exec -ti daoserver bash'
ddb () {
    docker exec -it $1 bash -c ' psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" '
}

db-usage () {
    docker exec -it $1 bash -c ' psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT schemaname,relname,n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC;" '
}

alias behat-commands='docker run -it --rm tournamentorganiser_systemtest behat -dl'

# Add dev data to tournament organiser
alias dev-data='docker exec -it database bash -c '"'"'psql --file=/docker-entrypoint-initdb.d/data/dev/behaviour_test_data.sql -U "$POSTGRES_USER" -d "$POSTGRES_DB" '"'"' '

alias lint='reset; eslint node; jshint $(find test/ -iname "*.js"); pylint $(find . -iname "*.py"); echo $?'

mcd () {
    mkdir -p $1
    cd $1
}
