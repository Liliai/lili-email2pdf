import email, os
from lib.eml2html import EmailtoHtml
from lib.html2pdf import HtmltoPdf



class EmlToPdfConvertor:
    def __init__(self, output_dir):
        self._email_to_html_convertor = EmailtoHtml()
        self._html_to_pdf_convertor = HtmltoPdf()
        self._output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    """
    Convert eml files to pdf files.
    """
    def convert(self, input_path, input_filenames):
        for filename in input_filenames:
            # read eml file
            input_filename = os.path.join(input_path, filename)
            with open(input_filename, 'r', encoding='ISO-8859-1') as f:
                eml_content = f.read()

            # convert eml to html
            email_message = email.message_from_string(eml_content)
            html = self._email_to_html_convertor.convert(email_message)
            html = """<div style="width:21cm; word-break: normal">"""+ html + "</div>"

            # convert html to pdf
            pdf_path = self._html_to_pdf_convertor.save_pdf(html.encode(), self._output_dir, filename + '.pdf')

