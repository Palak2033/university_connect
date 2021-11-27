from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Backend class to manage email authentication
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """Authentication method

        Parameters:
        -----------
        username : str
            Email of the user logging in
        password : password
            Password of the user logging in

        Returns:
        --------
        user : UserModel
            UserModel object which represents the user
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
