from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.follow import FollowResource
from resources.memo import MemoListResource, MemoResource, FollowMemoListResource
from resources.user import UserLoginResource, UserRegisterResource, UserLogoutResource
from resources.user import jwt_blacklist

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) : 
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

api.add_resource(UserRegisterResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserLogoutResource, '/user/logout')

api.add_resource(MemoListResource, '/memo')
api.add_resource(MemoResource, '/memo/<int:memo_id>')

api.add_resource(FollowResource, '/follow/<int:followee_id>')
api.add_resource(FollowMemoListResource, '/follow/memo')

if __name__ == '__main__' :
    app.run()