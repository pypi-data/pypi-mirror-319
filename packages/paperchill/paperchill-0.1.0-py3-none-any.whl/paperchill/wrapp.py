import os
from pathlib import Path
from typing import List, Optional

from flask import (
    Flask, flash, request, redirect, url_for, Request, make_response, render_template
)
from markdown2 import markdown
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest

from paperchill.chatbot import Chatbot
from paperchill.pdf_convert import pdf_convert
from paperchill.with_logger import WithLogger

ALLOWED_EXTENSIONS = {'pdf'}


class WrApp(WithLogger):
    def __init__(self, app: Flask):
        self.app = app
        self.chatbot = Chatbot(app.logger)
        super().__init__(app.logger)

    def upload(self, req: Request) -> Response:
        if req.method == 'POST':
            # check if the post request has the file part
            if 'file' not in req.files:
                flash('No file part')
                return redirect(req.url)
            file = req.files['file']
            # If user does not select a file, the browser submits an empty file without a filename
            if file.filename == '':
                flash('No selected file')
                return redirect(req.url)
            if file and is_allowed_filetype(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download', name=filename))
        return make_response(render_template('upload_form.html'))

    def display_file(self, name: str) -> str:
        text = pdf_convert(self.app, Path(self.app.config['UPLOAD_FOLDER']) / name)
        self.info(f'{len(text)} characters starting with {text[:80]}')
        summary = self.chatbot.summarize(text)
        questions = self.chatbot.get_questions(text, summary)
        return htmlify(text, summary, questions)

    def get_answer(self) -> str:
        if request.method == 'POST':
            question = self.get_asked_question()

            suggested_questions = list(set(get_suggested_questions(request.form)) - {question})

            answer = self.chatbot.get_answer(question, request.form['full_text'])
            rendered_answer = markdown(answer)

            return htmlify(
                request.form['full_text'],
                request.form['summary'],
                suggested_questions,
                question,
                [rendered_answer]
            )
        raise BadRequest(f'Method {request.method} not allowed')

    def get_asked_question(self):
        question = request.form.get('question')
        if not question:
            question = request.form.get('preselected_question', '')
        if not question:
            raise BadRequest('No question provided')
        self.info(f'question: {question}')
        return question


def get_suggested_questions(form: ImmutableMultiDict[str, str]) -> List[str]:
    return [
        form.get(f'suggested_question_{i}', '')
        for i in range(0, 5)
        if form.get(f'suggested_question_{i}')
    ]


def is_allowed_filetype(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def htmlify(
        text: str, summary: str,
        suggested_questions: List[str], asked_question: Optional[str] = None,
        answers: Optional[List[str]] = None
) -> str:
    summary_lines = summary.split('\n')
    return render_template(
        'summary_with_questions.html',
        summary_lines=summary_lines, text=text, summary=summary,
        suggested_questions=suggested_questions, asked_question=asked_question,
        answers=answers
    )
