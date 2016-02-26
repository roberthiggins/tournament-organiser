require 'ostruct'

class TournamentsController < ApplicationController

    include DaoConnection

    def index
        @tournaments = JSON.parse(
            from_dao('listtournaments').body)["tournaments"]
        @tournaments.map! { |tournament| Tournament.new(tournament) }
    end

    def show
        @tournament = Tournament.find(params[:id])
    end
end
