from Project.model.base_model import Model


class user_Model(Model):

    # Using private methods for creating the databases. They are to be used only by the class itself(not outside of it)
    # so this encapsulates it to be used only by it's methods.#
    @classmethod
    def _create_table(cls):
        with cls.connection as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS users (u_id SERIAL PRIMARY KEY,"
                                  "email TEXT UNIQUE NOT NULL, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, admin BOOLEAN)")
            conn.commit()


    @classmethod
    def insert_user(cls, email, username, password):
        with cls.connection as conn:
            conn.cursor().execute("INSERT INTO users(email,username,password) VALUES(%s,%s,%s);",
                                  (email, username, password,))
            conn.commit()

    @classmethod
    def get_user(cls, user_id):
        with cls.connection as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE u_id = %s;", (user_id,))
            res = cur.fetchone()
            return res

    @classmethod
    def get_all_users(cls):
        with cls.connection as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users;")
            res = cur.fetchall()
            return res

    @classmethod
    def delete_user(cls, id):
        try:
            with cls.connection as conn:
                conn.cursor().execute("DELETE FROM users WHERE u_id = %s;", (id,))
                conn.commit()
        except:
            return None