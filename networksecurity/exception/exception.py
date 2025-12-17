import sys
import traceback
from networksecurity.logging.logger import logging


class NetworkSecurityException(Exception):
    def __init__(self, error_message: Exception, error_details: sys = None):
        super().__init__(str(error_message))
        self.error_message = str(error_message)
        # Use provided error_details (sys) or current exc_info
        exc_type, exc_obj, exc_tb = (None, None, None)
        if error_details:
            try:
                exc_type, exc_obj, exc_tb = error_details.exc_info()
            except Exception:
                exc_type, exc_obj, exc_tb = sys.exc_info()
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()

        if exc_tb:
            # walk to last traceback frame
            last_tb = exc_tb
            while last_tb.tb_next:
                last_tb = last_tb.tb_next
            self.lineno = last_tb.tb_lineno
            self.file_name = last_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

    def __str__(self):
        return f"Error occurred in script name [{self.file_name}] line number [{self.lineno}] error message [{self.error_message}]"


if __name__ == '__main__':
    try:
        a = 1 / 0
    except Exception as e:
        logging.exception('Test exception')

