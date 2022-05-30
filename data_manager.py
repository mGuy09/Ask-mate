from psycopg2.extras import RealDictCursor
import connection


@connection.connection_handler
def get_data_question(cursor):
    cursor.execute("SELECT * FROM question;")
    return cursor.fetchall()


@connection.connection_handler
def get_data_answer(cursor, question_id):
    cursor.execute(
        "SELECT * FROM answer WHERE question_id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@connection.connection_handler
def get_question(cursor, id):
    cursor.execute(
        "SELECT id, submission_time, view_number, vote_number, title, message, image FROM question WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@connection.connection_handler
def get_answer(cursor, id):
    cursor.execute(
        "SELECT * FROM answer WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@connection.connection_handler
def add_question(cursor, title, message, image):
    cursor.execute(
        """
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
            VALUES (now()::timestamp(0),0,0, %(title)s, %(message)s,%(image)s) RETURNING id;
        """,
        {
            "title": title,
            "message": message,
            "image": image,
        },
    )
    return cursor.fetchone()["id"]


@connection.connection_handler
def add_data_answer(cursor, question_id, message, image):
    cursor.execute(
        """
            INSERT INTO answer(submission_time, vote_number, question_id, message, image)
            VALUES (now()::timestamp(0),0,%(question_id)s, %(message)s,%(image)s) RETURNING question_id;
        """,
        {
            "question_id": question_id,
            "message": message,
            'image':image
        },

    )
    return cursor.fetchone()['id']


@connection.connection_handler
def sort_question_data(cursor, sorting, direction, modifier):
    cursor.execute(
        f"SELECT * FROM question ORDER BY {sorting} {direction} LIMIT {modifier};"
    )
    return cursor.fetchall()


@connection.connection_handler
def delete_data(cursor, id):
    cursor.execute("DELETE FROM question WHERE id = %(id)s", {"id": id})


@connection.connection_handler
def delete_answer(cursor, id):
    cursor.execute(
        "DELETE FROM answer WHERE id = %(id)s RETURNING question_id",
        {"id": id},
    )
    return cursor.fetchone()["question_id"]


@connection.connection_handler
def delete_comment(cursor, id):
    cursor.execute(
        "DELETE FROM COMMENT WHERE id = %(id)s;",
        {"id": id},
    )


@connection.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    cursor.execute(
        "DELETE FROM COMMENT WHERE answer_id = %(answer_id)s;",
        {"answer_id": answer_id},
    )


@connection.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    cursor.execute(
        "DELETE FROM COMMENT WHERE question_id = %(question_id)s;",
        {"question_id": question_id},
    )


@connection.connection_handler
def delete_answers_by_question(cursor, question_id):
    return cursor.execute(
        "DELETE FROM answer WHERE question_id=%(question_id)s RETURNING id;",
        {"question_id": question_id},
    )


@connection.connection_handler
def update_data_question(cursor, id, title, message):
    cursor.execute(
        "UPDATE question SET title = %(title)s, message = %(message)s, submission_time = now()::timestamp(0) WHERE id = %(id)s;",
        {
            "title": title,
            "message": message,
            "id": id,
        },
    )


@connection.connection_handler
def update_data_answer(cursor, id, message):
    cursor.execute(
        "UPDATE answer SET message = %(message)s, submission_time = now()::timestamp(0) WHERE id = %(id)s;",
        {
            "message": message,
            "id": id,
        },
    )


@connection.connection_handler
def update_comments(cursor, id, message):
    cursor.execute(
        "UPDATE COMMENT SET message = %(message)s, edited_count = edited_count + 1, submission_time = now()::timestamp(0) WHERE id = %(id)s",
        {
            "message": message,
            "id": id,
        },
    )


@connection.connection_handler
def vote_item(cursor, table, id, modifier):
    cursor.execute(
        f"UPDATE {table} SET vote_number = vote_number + %(modifier)s WHERE id = %(id)s;",
        {
            "modifier": modifier,
            "id": id,
        },
    )


def vote_on_question(id, modifier):
    vote_item("question", id, modifier)


def vote_on_answer(id, modifier):
    vote_item("answer", id, modifier)


@connection.connection_handler
def add_comment(cursor, question_id, message):
    cursor.execute(
        "INSERT INTO comment (question_id, message, submission_time, edited_count) VALUES (%(question_id)s, %(message)s, now(), 0);",
        {
            "question_id": question_id,
            "message": message,
        },
    )


@connection.connection_handler
def get_comment(cursor, question_id):
    cursor.execute(
        "SELECT * FROM COMMENT WHERE question_id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@connection.connection_handler
def get_question_comment(cursor, id):
    cursor.execute(
        "SELECT * FROM COMMENT WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute(
        "SELECT * FROM answer WHERE id = %(answer_id)s;",
        {"answer_id": answer_id},
    )
    return cursor.fetchall()


@connection.connection_handler
def add_comment_answer(cursor, answer_id, message):
    cursor.execute(
        """
            INSERT INTO comment(answer_id, message, submission_time, edited_count)
            VALUES(%(answer_id)s, %(message)s, now(), 0) RETURNING id;
        """,
        {"answer_id": answer_id, "message": message},
    )
    return cursor.fetchone()


@connection.connection_handler
def get_comment_answer(cursor, answer_id):
    cursor.execute(
        "SELECT * FROM COMMENT WHERE answer_id = %(answer_id)s;",
        {"answer_id": answer_id},
    )
    return cursor.fetchall()


@connection.connection_handler
def get_all_comments(cursor):
    cursor.execute("SELECT * FROM comment;")
    return cursor.fetchall()


@connection.connection_handler
def search_question(cursor, search_phrase):
    cursor.execute(
        """
            SELECT *
            FROM question
            WHERE lower(question.title) LIKE CONCAT('%', lower(%(search_phrase)s), '%')
            OR lower(question.message) LIKE CONCAT('%', lower(%(search_phrase)s), '%');
        """,
        {"search_phrase": search_phrase},
    )
    return cursor.fetchall()


@connection.connection_handler
def search_answer(cursor, search_phrase):
    cursor.execute(
        """
            SELECT *
            FROM answer
            WHERE answer.message LIKE CONCAT('%', lower(%(search_phrase)s), '%');   
        """,
        {"search_phrase": search_phrase},
    )
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
def add_question_tag(cursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag(question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s )
    """
    values = {"question_id": question_id, "tag_id": tag_id}
    cursor.execute(query, values)


@connection.connection_handler
def add_new_tag(cursor, name):
    query = """
    INSERT INTO tag (name)
    VALUES (%(name)s)
    """
    values = {"name": name}
    cursor.execute(query, values)


@connection.connection_handler
def get_tag_by_question_id(cursor, question_id):
    query = """
        select *
        from tag
        join question_tag qt on tag.id = qt.tag_id
        where qt.question_id = %(question_id)s and qt.tag_id = tag.id
    """
    values = {"question_id": question_id}
    cursor.execute(query, values)
    return cursor.fetchone()


@connection.connection_handler
def check_if_tag_exists(cursor, question_id, tag_id):
    query = """
        select *
        from tag
        
            
    """


@connection.connection_handler
def get_all_tags_by_question_id(cursor, question_id):
    cursor.execute(
        """
            SELECT *
            FROM tag
            JOIN question_tag ON tag.id = question_tag.tag_id
            WHERE question_tag.question_id = %(question_id)s AND question_tag.tag_id = tag.id;
        """,
        {"question_id": question_id},
    )
    return cursor.fetchall()


@connection.connection_handler
def get_tag_from_id(cursor, tag_id):
    cursor.execute("SELECT * FROM tag WHERE id = %(tag_id)s;", {"tag_id": tag_id})
    return cursor.fetchone()


@connection.connection_handler
def delete_tag(cursor, tag_id, question_id):
    cursor.execute(
        "DELETE FROM question_tag WHERE tag_id = %(tag_id)s AND question_id = %(question_id)s;",
        {
            "tag_id": tag_id,
            "question_id": question_id,
        },
    )


@connection.connection_handler
def delete_tags_from_question(cursor, question_id):
    cursor.execute(
        "DELETE FROM question_tag WHERE question_id = %(question_id)s",
        {"question_id": question_id},
    )


@connection.connection_handler
def get_tag_from_question_tag(cursor, question_id, tag_id):
    cursor.execute(
        "SELECT * FROM question_tag WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s;",
        {
            "question_id": question_id,
            "tag_id": tag_id,
        },
    )
    return cursor.fetchone()


@connection.connection_handler
def add_user(cursor,email,username,password):
    query = """
    INSERT INTO user_data (registration_time,reputation,email,username,password)
    VALUES (now()::timestamp(0),0,%(email)s,%(username)s,%(password)s)
    """
    values = {"email": email,
              "username": username,
              "password": password
              }

    cursor.execute(query, values)


@connection.connection_handler
def get_user(cursor, email_or_name):
    query = '''
        select * from user_data ud
        where ud.email = %(email_or_name)s or ud.username = %(email_or_name)s
    '''
    cursor.execute(query, {'email_or_name': email_or_name})
    return cursor.fetchone()


@connection.connection_handler
def add_question_and_user(cursor,question_id,user_id):
    query = '''
        insert into question_user_id (question_id, user_id)
        values (%(question_id)s,%(user_id)s)
    '''
    values = {
        'question_id':question_id,
        'user_id': user_id
    }
    cursor.execute(query,values)


@connection.connection_handler
def add_answer_and_user(cursor, answer_id, user_id):
    query = '''
        insert into answer_user_id (answer_id, user_id)
        values (%(answer_id)s,%(user_id)s)
    '''
    values = {
        'answer_id': answer_id,
        'user_id': user_id
    }
    cursor.execute(query, values)


@connection.connection_handler
def add_comment_and_user(cursor, comment_id, user_id):
    query = '''
        insert into comment_user_id (comment_id, user_id)
        values (%(comment_id)s,%(user_id)s)
    '''
    values = {
        'comment_id': comment_id,
        'user_id': user_id
    }
    cursor.execute(query, values)