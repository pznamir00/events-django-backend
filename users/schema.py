import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery


class AuthMutation(graphene.ObjectType):
    #tokens
    verify_token = mutations.VerifyToken.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    #account
    register = mutations.Register.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    delete_account = mutations.DeleteAccount.Field()
    #password reset
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass