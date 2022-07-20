import os
import json
from datetime import datetime
import logging as log

class FilePipeline:

    def open_spider(self, spider):
        self.file = open(os.path.join(os.getenv('TO_FILE_FOLDER', ""), spider.name + '_' + datetime.now().strftime("%Y%m%d%H%M%S")), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        log.info('Writing to file storage')

        line = json.dumps(item) + "\n"
        self.file.write(line)

        return item
