from Project.model.DB import Session


def on_failed_job(job, connection, type, value, traceback):
    # Return session to DB pool
    Session.remove()

    return