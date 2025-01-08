import os
from pathlib import Path

from flask import Flask
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


def pdf_convert(app: Flask, pdf_file: Path):
    converter = PdfConverter(artifact_dict=create_model_dict())
    app.logger.info('converter created')

    app.logger.info(f'converting {pdf_file} ({os.stat(pdf_file).st_size} bytes)')
    rendered = converter(str(pdf_file))
    text, _, _ = text_from_rendered(rendered)
    app.logger.info(f'converted {pdf_file} to {len(text)} characters')

    return text
