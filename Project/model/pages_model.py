from Project.model.base_model import Model


class pages_Model(Model):
    '''
     This is the class used for accessing and managing the DataBase. It uses a PostgreSQL database,
     which is quite sufficient for the scope of the app, especially when we have to package it for distribution.
     It's used for CRUD operations such as:
     -store, retrieve and delete facebook pages
     -store,retrieve and delete users
    '''

    # Using private methods for creating the databases. They are to be used only by the class itself(not outside of it)
    # so this encapsulates it to be used only by it's methods.#
    @classmethod
    def _create_table(cls):
        with cls.connection as conn:
            conn.cursor().execute("CREATE TABLE IF NOT EXISTS pages (id SERIAL PRIMARY KEY UNIQUE,"
                                  "page_name TEXT NOT NULL, "
                                  "page_id TEXT UNIQUE NOT NULL,"
                                  "account_id INT NOT NULL,"
                                  "CONSTRAINT account_id"
                                  "     FOREIGN KEY( account_id)"
                                  "         REFERENCES accounts(acc_id)"
                                  "         ON DELETE CASCADE)")
            conn.commit()

    # Class methods are being used instead of instance methods, because we're dealing with the class directly,
    # and there is only one variation of it, e.g no need to instantiate it to create different instances, that
    # have different properties (different settings) - at least this is not needed in this case.#

    @classmethod
    def insert_page(cls, page_id, name,acc_id):
        name = str(name).lower()
        with cls.connection as conn:
            conn.cursor().execute("INSERT INTO pages(page_name,page_id,account_id) VALUES(%s,%s,%s);", (name, page_id,acc_id))
            conn.commit()

    @classmethod
    def get_page(cls, name=None, id=None,acc_id=None):
        # Supporting search trough id or name of the FB page.
        with cls.connection as conn:
            cur = conn.cursor()
            if id:
                cur.execute("SELECT * FROM pages WHERE page_id = %s;", (id,))
                return cur.fetchone()
            if acc_id:
                cur.execute("SELECT * FROM pages WHERE account_id = %s;", (acc_id,))
                return cur.fetchall()
            if name:
                name = str(name).lower()
                cur.execute("SELECT * FROM pages WHERE page_name LIKE %s;", (name[:6] + "%",))
                return cur.fetchall()
            # If nothing is specified get all the entries in the pages table.
            else:
                return cls.get_all_pages()

    # Creating an explicit method for getting all entries from the pages table.
    @classmethod
    def get_all_pages(cls):
        with cls.connection as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pages;")
            return cur.fetchall()

    @classmethod
    def delete_page(cls, id):
        try:
            with cls.connection as conn:
                conn.cursor().execute("DELETE FROM pages WHERE page_id = %s;", (id,))
                conn.commit()
        except:
            return None

    @classmethod
    def master_delete_all_pages(cls):
        try:
            with cls.connection as conn:
                conn.cursor().execute("TRUNCATE TABLE pages RESTART IDENTITY;")
                conn.commit()
        except:
            return None











if __name__ == "__main__":
    Model.create_all_tables()
    Model.master_delete_all_pages()
    Model.insert_user("bogo@test.bg","Bogo",123456)
    Model.insert_user("bogo@testing.bg","Bogot",123456)
    Model.insert_account("Skoda","skoda@test.bg","Sample email",1)
    Model.insert_account("Skoda","skoda@testing.bg","Sample email",2)
    Model.insert_page(1189230704429977, "DEV.bg",1)
    Model.insert_page(140269359421625, "Nik",1)
    Model.insert_page(1402693594216250, "Nik",2)
    Model.insert_page(14026935942162500, "Nik",2)
    Model.insert_page(181039705377403, "Sportvision",2)
    # result = Model.get_all()
    res = Model.get_page(name="n")
    print(res)
    # print(result)
