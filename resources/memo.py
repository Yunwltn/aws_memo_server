from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error


class MemoListResource(Resource) :
    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()
        # 클라이언트에서 쿼리스트링으로 보내는 데이터는 request.args에 들어있다
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select id, title, datetime, content, createdAt, updatedAt
                    from memo
                    where userId= %s
                    order by datetime desc
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''
                    # 컬럼은 ~다에만 %s 사용

            record = (user_id, )

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['datetime'] = row['datetime'].isoformat()
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200

    @jwt_required()
    def post(self) : 
        # {"title": "1월 약속",
        # "datetime": "2023-05-16",
        # "content": "친구 만나기"}
    
        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''insert into memo(userId, title, datetime, content)
                    values(%s, %s, %s, %s);'''

            record = ( user_id, data['title'], data['datetime'], data['content'])

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success"}, 200

class MemoResource(Resource) :
    @jwt_required()
    def delete(self, memo_id) :

        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = ''' delete from memo
                    where id = %s and userId = %s ; '''
            
            record = (memo_id, user_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success"}, 200

    @jwt_required()
    def put(self, memo_id) :
        # {"title" : "제목",
        # "datetime" : "2023-01-22",
        # "content" : "내용"}

        data = request.get_json()
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = ''' update memo
                    set
                    title= %s,
                    datetime= %s,
                    content= %s
                    where id = %s and userId= %s; '''

            record = (data['title'], data['datetime'], data['content'], memo_id, user_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success"}, 200

class FollowMemoListResource(Resource) :
    @jwt_required()
    def get(self) :
        user_id = get_jwt_identity()

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select u.nickname, m.title, m.datetime, m.content, m.createdAt, f.followeeId, m.id as memoId
                    from follow as f
                    join user as u on f.followerId = u.id
                    join memo as m on m.userId = f.followeeId
                    where f.followerId = %s
                    order by m.datetime desc
                    limit ''' + offset + ''' , ''' + limit + ''' ; '''

            record = ( user_id, )

            cursor = connection.cursor(dictionary= True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['datetime'] = row['datetime'].isoformat()
                result_list[i]['createdAt'] = row['createdAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"result" : "fail", "error" : str(e)}, 500

        return {"result" : "success", "items" : result_list, "count" : len(result_list)}, 200