import os
import json
from datetime import datetime
import logging as log

class FilePipeline:

    def open_spider(self, spider):
        self.file_path = os.path.join(os.getenv('TO_FILE_FOLDER', ""), spider.name + '_' + datetime.now().strftime("%Y%m%d%H%M%S"))
        self.file = open(self.file_path, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        log.info('Writing to file storage on: %s' % self.file_path)

        line = json.dumps(item) + "\n"
        self.file.write(line)

        return item
