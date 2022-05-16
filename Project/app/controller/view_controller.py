from Project.model.DB import Session
from flask import send_file
from Project.model.all_models import ScreenShotModel
import os


def show_pdf(id):
    # Create Session
    db_sess = Session()

    # Find the pdf
    result = ScreenShotModel.search(db_sess, { "account_id": f"=,{id}" })

    if not result:
        return "<h1>No PDF found</h1>"

    return send_file(result[0].file_dir, attachment_filename='screenshot.pdf')