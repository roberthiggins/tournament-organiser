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

    def new
        @tournament = Tournament.new
    end

    def create
        @tournament = Tournament.new(tournament_params)

        response = from_dao('addTournament', {
            :inputTournamentName => @tournament.name,
            :inputTournamentDate => @tournament.date
        })

        if response.code.to_i == 200
            render 'show'
        else
            render 'new'
        end
    end

    private
        def tournament_params
            params.require(:tournament).permit(:name, :date, :rounds)
        end
end
