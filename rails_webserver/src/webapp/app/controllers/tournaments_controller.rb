require 'ostruct'

class TournamentsController < ApplicationController

    include DaoConnection

    def index
        @tournaments = JSON.parse(dao_get('listtournaments').body)["tournaments"]
        @tournaments.map! { |tournament| Tournament.new(tournament) }
    end
end
