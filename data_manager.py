from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import datetime
import connection


@connection.connection_handler
def get_data_question(cursor):
    query = '''
        select * 
        from question
    '''
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def get_data_answer(cursor, question_id):
    query = '''
        select *
        from answer where question_id = %(question_id)s
    '''
    value = {"question_id": question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def get_question(cursor: RealDictCursor, id:int):
    query = f'''
        select id,submission_time,view_number,vote_number,title,message,image
        from question
        where id = {id}
    '''
    # value = {'id': id}
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def get_answer(cursor: RealDictCursor, id:int):
    query = '''
        select *
        from answer
        where id = %(id)s'''
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchone()

@connection.connection_handler
def add_question(cursor,title,message,image):
    query = f'''
        insert into question(submission_time,view_number,vote_number,title,message,image)
        values (now(),0,0, '{title}' , '{message}' ,'{image}')
        returning id;
    '''
    # value = {'tile':title,'message':message,'image':image}
    cursor.execute(query)
    id = cursor.fetchone()['id']
    return id


@connection.connection_handler
def add_data_answer(cursor,question_id,message, image):
    query = f'''
        insert into answer(submission_time,vote_number,question_id,message,image)
        values (now(),0,{question_id}, '{message}' ,'{image}')
        returning question_id
    '''
    # value = {'question_id':question_id,'message':message}
    cursor.execute(query)
    # id = cursor.fetchone()['question_id']
    # return id


@connection.connection_handler
def sort_question_data(cursor,sorting,direction):
    query = f'''
        select *
        from question
        order by {sorting} {direction};
    '''
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_data(cursor, id):
    query= """
    Delete from question where id = %(id)s
    """
    value = {'id': id}
    cursor.execute(query, value)

@connection.connection_handler
def delete_answer(cursor,id):
    query = '''
        delete from answer where id = %(id)s
        returning question_id
    '''
    value = {'id':id}
    cursor.execute(query,value)
    question_id = cursor.fetchone()['question_id']
    return question_id


@connection.connection_handler
def delete_answers_by_question(cursor, question_id):
    query = '''
        delete from answer where question_id=%(question_id)s
    '''
    value = {'question_id': question_id}
    cursor.execute(query, value)


@connection.connection_handler
def update_data_question(cursor,id,title,message):
    cursor.execute('''
    Update question SET title = %s, message = %s where id = %s ''',(title,message,id))


@connection.connection_handler
def vote_on_question(cursor,id,modifier):
    query = f'''
        update question set vote_number = vote_number + {modifier} 
        where id ={id}
    '''
    cursor.execute(query)


@connection.connection_handler
def vote_on_answer(cursor,id,modifier):
    query = f'''
        update answer set vote_number = vote_number + {modifier} 
        where id ={id}
    '''
    cursor.execute(query)

@connection.connection_handler
def add_comment(cursor, question_id, message):
    query = f'''
    INSERT INTO comment(question_id,  message, submission_time, edited_count)
    VALUES({question_id}, '{message}', now(), 0)
    returning question_id
    '''
    cursor.execute(query)


@connection.connection_handler
def get_comment(cursor: RealDictCursor, question_id):
    query = """
    SELECT  *
    FROM comment WHERE  question_id = %(question_id)s;
    """
    value = {'question_id':question_id}
    cursor.execute(query, value)
    return cursor.fetchall()


# def get_data(csv_file):
#     return connection.read_question(csv_file)
#
#
# def sort_asc(csv_file, order_value, order_direction):
#     direction = "desc" if order_value in ["view_number", "vote_number"] else "asc"
#
#     csv_data = sorted(
#         get_data(csv_file),
#         key=lambda row: row[order_value],
#         reverse=(order_direction == direction),
#     )
#
#     for i in csv_data:
#         i["submission_time"] = util.convert_time(i["submission_time"])
#
#     return csv_data
#
#
# def remove_question(data_csv, id):
#     question_list = connection.read_question(data_csv)
#     for i in question_list:
#         if i["id"] == id:
#             question_list.remove(i)
#     connection.delete_question(data_csv, question_list)
#
#
# def remove_answer(data_csv, id):
#     answer_list = connection.read_question(data_csv)
#     for i in answer_list:
#         if i["id"] == id:
#             deleted_answer = i
#     question_id = deleted_answer["question_id"]
#     answer_list.remove(deleted_answer)
#     connection.delete_answer(data_csv, answer_list)
#     return question_id
