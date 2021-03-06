from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
    
from captionstransformer import core
from .htmlescape import htmlescape

class Reader(core.Reader):
    def text_to_captions(self):
        try:
            soup = BeautifulSoup(self.rawcontent,"html.parser")
        except AttributeError:
            soup = BeautifulSoup(self.rawcontent,convertEntities=BeautifulSoup.HTML_ENTITIES)
        texts = soup.findAll('p')
        for text in texts:
            caption = core.Caption()
            caption.start = self.get_date(text['begin'])
            caption.end = self.get_date(text['end'])
            caption.text = text.text
            self.add_caption(caption)

        return self.captions

    def get_date(self, time_str):
        return datetime.strptime(time_str, '%H:%M:%S.%f')

class Writer(core.Writer):
    DOCUMENT_TPL = u"""<tt xml:lang="" xmlns="http://www.w3.org/ns/ttml"><body><div>%s</div></body></tt>"""
    CAPTION_TPL = u"""<p begin="%(start)s" end="%(end)s">%(text)s</p>"""

    def format_time(self, caption):
        """Return start and end time for the given format"""
        #should be seconds by default

        return {'start': caption.start.strftime('%H:%M:%S.%f')[:-3],
                'end': caption.end.strftime('%H:%M:%S.%f')[:-3]}
    
    def get_template_info(self, caption):
        info = self.format_time(caption)
        info['text'] = htmlescape(caption.text)
        return info
