class RegistrationsController < Devise::RegistrationsController
    include DaoConnection

      def new
        super
      end

      def create

        # We need to check if the user exists in the dao.
        response = from_dao('/addPlayer', user_params)
        if response.code.to_i == 200
            super
        end
        # If so we error as appropriate
        @user.errors[:base] << response.body
      end

      def update
        super
      end

    private
        def user_params
            params.require(:user).permit(:email, :password, :password_confirmation)
        end

end 
