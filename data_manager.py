from psycopg2.extras import RealDictCursor
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
def get_answer(cursor: RealDictCursor, id):
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
def sort_question_data(cursor,sorting,direction, modifier):
    query = f'''
        select *
        from question
        order by {sorting} {direction}
        limit {modifier};
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
def delete_comment(cursor,id):
    query = '''
        delete from comment where id = %(id)s
    '''
    value = {'id': id}
    cursor.execute(query,value)


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
    Update question SET title = %s, message = %s, submission_time = now()::timestamp(0)where id = %s ''',(title,message,id))


@connection.connection_handler
def update_data_answer(cursor,id,message):
    cursor.execute('''
    update answer set message = %s, submission_time = now()::timestamp(0) where id = %s 
    ''',(message,id))


@connection.connection_handler
def update_comments(cursor,id,message):
    cursor.execute(f'''
    update comment set message = '{message}', edited_count = edited_count +1 , 
    submission_time = now()::timestamp(0) where id = {id}
    ''')


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


@connection.connection_handler
def get_question_comment(cursor,id):
    query = f'''
    select *
    from comment where id = {id}
    '''
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def get_answer_by_id(cursor, id):
    query = """
    SELECT *
    FROM answer
    WHERE id = %(answer_id)s
    """
    value = {'id': id}
    cursor.execute(query, value)
    return cursor.fetchall()


@connection.connection_handler
def add_comment_answer(cursor, answer_id, message):
    query = '''
        INSERT INTO comment( answer_id,  message, submission_time, edited_count)
        VALUES( %(answer_id)s, %(message)s, now(), 0) 
        RETURNING id;
        '''
    cursor.execute(query, dict(answer_id=answer_id, message=message))
    return cursor.fetchone()


@connection.connection_handler
def get_comment_answer(cursor: RealDictCursor, answer_id):
    query = """
    SELECT  *
    FROM comment WHERE  answer_id = %(answer_id)s;
    """
    value = {'answer_id':answer_id}
    cursor.execute(query, value)
    return cursor.fetchall()

@connection.connection_handler
def get_all_comments(cursor):
    query = """
            SELECT *
            FROM comment
            """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def search_question(cursor,search_phrase):
    query = f'''
        select *
        from question
        where question.title like '%{search_phrase}%%' OR
        question.message like '%{search_phrase}%%';
    '''
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search_answer(cursor, search_phrase):
    query = f'''
        select *
        from answer
        where answer.message like '%{search_phrase}%%'    
    '''
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def get_tags(cursor):
    query = """
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def add_question_tags(cursor, question_id, tag_id ):
    query = """
    INSERT INTO question_tag(question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s )
    """
    values = {'question_id': question_id, 'tag_id': tag_id}
    cursor.execute(query, values)

@connection.connection_handler
def add_new_tag(cursor, name):
    query = """
    INSERT INTO tag (name)
    VALUES (%(name)s)
    """
    values = {'name': name}
    cursor.execute(query, values)


@connection.connection_handler
def get_tag_by_question_id(cursor, question_id):
    query = '''
        select *
        from tag
        join question_tag qt on tag.id = qt.tag_id
        where qt.question_id = %(question_id)s and qt.tag_id = tag.id
    '''
    values = {'question_id': question_id}
    cursor.execute(query, values)
    return cursor.fetchone()


@connection.connection_handler
def get_all_tags_by_question_id(cursor, question_id):
    query = '''
        select *
        from tag
        join question_tag qt on tag.id = qt.tag_id
        where qt.question_id = %(question_id)s and qt.tag_id = tag.id
    '''
    values = {'question_id': question_id}
    cursor.execute(query, values)
    return cursor.fetchall()

@connection.connection_handler
def get_tag_from_id(cursor, tag_id):
    query = '''
            select *
            from tag
            where id = %(tag_id)s
        '''
    values = {'tag_id': tag_id}
    cursor.execute(query, values)
    return cursor.fetchone()


@connection.connection_handler
def delete_tag(cursor, tag_id, question_id):
    query = '''
        delete 
        from question_tag where tag_id = %(tag_id)s and question_id = %(question_id)s;
    '''
    values = {'tag_id': tag_id, 'question_id': question_id}
    cursor.execute(query, values)
