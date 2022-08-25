import os
import extract_msg
from lib.html2pdf import HtmltoPdf
from lib.eml2html import EmailtoHtml


class MsgToPdfConvertor:
    def __init__(self, output_dir):
        self._email_to_html_convertor = EmailtoHtml()
        self._html_to_pdf_convertor = HtmltoPdf()        
        self._output_dir= output_dir
        os.makedirs(output_dir, exist_ok=True)


    def convert(self, input_path, input_filenames):
        for filename in input_filenames:
            input_filename = os.path.join(input_path, filename)
            with open(input_filename, "r", encoding="ISO-8859-1") as f:
                msg_content = f.read()
            msg = extract_msg.message.Message(input_filename)
            body = msg.body

            data = {}
            data["From : "] = msg.sender or ''
            data["Subject : "] = msg.subject or ''
            data["Date : "] = msg.date or ''
            receivers = msg.to or []
            if isinstance(receivers, str):
                receivers = receivers.split(',')
            data["To : "] = receivers
            ccs = msg.cc 
            if msg.cc :
                if isinstance(ccs, str):
                    ccs = ccs.split(',')
                data["Ccs : "] = ccs
            else :''
            print(data)


            htmlContent = """
            <html><head></head><body><div style="width:21cm; word-break: break-word">
            """
            for key , value in data.items():
                htmlContent = htmlContent + "<p><strong>{}</strong>{}</p>".format(key , value)
            htmlContent = htmlContent + """<pre>\n""" + body + "\n</pre></div></body></html>"""

            pdf_path = self._html_to_pdf_convertor.save_pdf(htmlContent.encode(), self._output_dir, filename + '.pdf')

