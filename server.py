import os
import tempfile

import cherrypy
from cherrypy.lib.static import serve_file

import pyoo


def create_temp_file(uploaded_file):
    out = tempfile.NamedTemporaryFile(delete=False, suffix='.ods')
    while True:
        data = uploaded_file.file.read(8192)
        if not data:
            break
        out.write(data)
    out.close()
    return out


def open_ods(file_path):
    desktop = pyoo.Desktop('localhost', 2002)
    doc = desktop.open_spreadsheet(file_path)
    return doc


class OdsApi(object):
    @cherrypy.expose
    def convert_to_pdf(self, file, **kwargs):
        """Convert ODS file to PDF"""
        ufile = create_temp_file(file)
        file_path = ufile.name
        pdf_path = file_path + '.pdf'

        doc = open_ods(file_path)
        doc.save(pdf_path, 'calc_pdf_Export', kwargs)
        doc.close()

        os.remove(file_path)

        return serve_file(pdf_path, 'application/x-download', 'attachment')

    @cherrypy.expose
    def calculate_all(self, file):
        """Calculate all formulas in ODS file"""
        ufile = create_temp_file(file)
        file_path = ufile.name

        doc = open_ods(file_path)
        doc.calculate_all()
        doc.save()
        doc.close()

        return serve_file(file_path, 'application/x-download', 'attachment')

    @cherrypy.expose
    def calculate_all_and_convert_to_pdf(self, file, **kwargs):
        ufile = create_temp_file(file)
        file_path = ufile.name
        pdf_path = file_path + '.pdf'

        doc = open_ods(file_path)
        doc.calculate_all()
        doc.save(pdf_path, 'calc_pdf_Export', kwargs)
        doc.close()

        os.remove(file_path)

        return serve_file(pdf_path, 'application/x-download', 'attachment')


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(OdsApi(), '/ods')
