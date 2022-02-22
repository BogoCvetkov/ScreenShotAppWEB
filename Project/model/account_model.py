from Project.model.base_model import Model

class account_Model(Model):

    # Using private methods for creating the databases. They are to be used only by the class itself(not outside of it)
    # so this encapsulates it to be used only by it's methods.#
    @classmethod
    def _create_table(cls):
        with cls.connection as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS accounts (acc_id SERIAL PRIMARY KEY UNIQUE,"
                                  "account_name TEXT NOT NULL,"
                                  "email TEXT UNIQUE NOT NULL,"
                                  "email_body TEXT,"
                                  "user_id INT NOT NULL,"
                                  "active BOOLEAN ,"
                                  "CONSTRAINT user_id"
                                  "     FOREIGN KEY (user_id)"
                                  "     REFERENCES users(u_id)"
                                  "     ON DELETE CASCADE)")
            conn.commit()

    @classmethod
    def insert_account(cls, name, email, email_body, user_id, active=True):
        with cls.connection as conn:
            conn.cursor().execute("INSERT INTO accounts(account_name, email, email_body, user_id, active) VALUES(%s,"
                                  "%s,%s,%s,%s);", (name, email,email_body,user_id, active,))
            conn.commit()

    @classmethod
    def get_account(cls, name=None, id=None,user_id = None):
        with cls.connection as conn:
            cur = conn.cursor()
            if id:
                cur.execute("SELECT * FROM accounts WHERE acc_id = %s;", (id,))
                return cur.fetchone()
            if user_id:
                cur.execute("SELECT * FROM accounts WHERE user_id = %s;", (user_id,))
                return cur.fetchall()
            if name:
                name = str(name).lower()
                cur.execute("SELECT * FROM accounts WHERE acc_name LIKE %s;", (name[:6] + "%",))
                return cur.fetchall()
            # If nothing is specified get all the entries in the pages table.
            else:
                cur.execute("SELECT * FROM accounts;",)
                return cur.fetchall()

    @classmethod
    def delete_account(cls, id):
        try:
            with cls.connection as conn:
                conn.cursor().execute("DELETE FROM accounts WHERE acc_id = %s;", (id,))
                conn.commit()
        except:
            return None
