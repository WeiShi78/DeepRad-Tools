from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QLineEdit, QTextBrowser
from PyQt5.QtGui import QTextCursor
# from MyPyQtGUI import MainApp
from queue import Queue

import logging
import datetime
import tqdm
import time
import sys

import tqdm.auto as t_AUTO

IS_SETUP_DONE = 'is_setup_done'

TQDM_WRITE_STREAM_CONFIG = 'TQDM_WRITE_STREAM_CONFIG'
STDOUT_WRITE_STREAM_CONFIG = 'STDOUT_WRITE_STREAM_CONFIG'
IS_STREAMS_REDIRECTION_SETUP_DONE = 'IS_STREAMS_REDIRECTION_SETUP_DONE'

STREAM_CONFIG_KEY_QUEUE = 'queue'
STREAM_CONFIG_KEY_STREAM = 'write_stream'
STREAM_CONFIG_KEY_QT_QUEUE_RECEIVER = 'qt_queue_receiver'

default_config_dict = {
    IS_SETUP_DONE: False,
    IS_STREAMS_REDIRECTION_SETUP_DONE: False,
    TQDM_WRITE_STREAM_CONFIG: None,
    STDOUT_WRITE_STREAM_CONFIG: None,
}

config_dict = default_config_dict

# DEFINITION NEEDED FIRST ...
class WriteStream(object):
    def __init__(self, q: Queue):
        self.queue = q

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass

class WhitespaceRemovingFormatter(logging.Formatter):
    def format(self, record):
        record.msg = record.msg.strip()
        return super(WhitespaceRemovingFormatter, self).format(record)

def setup_logging(log_prefix, force_debug_level=logging.DEBUG):

    root = logging.getLogger()
    root.setLevel(force_debug_level)

    if config_dict[IS_SETUP_DONE]:
        pass
    else:
        __log_file_name = "{}-{}_log_file.txt".format(log_prefix,
                                                      datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "-"))

        __log_format = '%(asctime)s - %(name)-s - %(levelname)s - %(message)s'
        __console_date_format = '%Y-%m-%d %H:%M:%S'
        __file_date_format = '%Y-%m-%d %H-%M-%S'

        console_formatter = WhitespaceRemovingFormatter(__log_format, __console_date_format)

        file_formatter = WhitespaceRemovingFormatter(__log_format, __file_date_format)
        file_handler = logging.FileHandler(__log_file_name, mode='a', delay=True)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        root.addHandler(file_handler)

        tqdm_handler = TqdmLoggingHandler()
        tqdm_handler.setLevel(logging.DEBUG)
        tqdm_handler.setFormatter(console_formatter)
        root.addHandler(tqdm_handler)

        config_dict[IS_SETUP_DONE] = True


class TqdmLoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        tqdm.tqdm.write(msg)
        self.flush()




class QueueWriteStream(object):
    def __init__(self, q: Queue):
        self.queue = q

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass


def perform_tqdm_default_out_stream_hack(tqdm_file_stream, tqdm_nb_columns=None):
    # save original class into module
    tqdm.orignal_class = tqdm.tqdm

    class TQDMPatch(tqdm.orignal_class):
        """
        Derive from original class
        """

        def __init__(self, iterable=None, desc=None, total=None, leave=True,
                     file=None, ncols=None, mininterval=0.1, maxinterval=10.0,
                     miniters=None, ascii=None, disable=False, unit='it',
                     unit_scale=False, dynamic_ncols=False, smoothing=0.3,
                     bar_format=None, initial=0, position=None, postfix=None,
                     unit_divisor=1000, gui=False, **kwargs):
            super(TQDMPatch, self).__init__(iterable, desc, total, leave,
                                            tqdm_file_stream,  # change any chosen file stream with our's
                                            tqdm_nb_columns,  # change nb of columns (gui choice),
                                            mininterval, maxinterval,
                                            miniters, ascii, disable, unit,
                                            unit_scale,
                                            False,  # change param
                                            smoothing,
                                            bar_format, initial, position, postfix,
                                            unit_divisor, gui, **kwargs)
            print('TQDM Patch called')  # check it works

        @classmethod
        def write(cls, s, file=None, end="\n", nolock=False):
            super(TQDMPatch, cls).write(s=s, file=file, end=end, nolock=nolock)
            #tqdm.orignal_class.write(s=s, file=file, end=end, nolock=nolock)

        # all other tqdm.orignal_class @classmethod methods may need to be redefined !

    # # I mainly used tqdm.auto in my modules, so use that for patch
    # # unsure if this will work with all possible tqdm import methods
    # # might not work for tqdm_gui !

    #
    # # change original class with the patched one, the original still exists
    t_AUTO.tqdm = TQDMPatch
    #tqdm.tqdm = TQDMPatch


def setup_streams_redirection(tqdm_nb_columns=None):
    if config_dict[IS_STREAMS_REDIRECTION_SETUP_DONE]:
        pass
    else:
        configure_tqdm_redirection(tqdm_nb_columns)
        configure_std_out_redirection()
        config_dict[IS_STREAMS_REDIRECTION_SETUP_DONE] = True


def configure_std_out_redirection():
    queue_std_out = Queue()
    config_dict[STDOUT_WRITE_STREAM_CONFIG] = {
        STREAM_CONFIG_KEY_QUEUE: queue_std_out,
        STREAM_CONFIG_KEY_STREAM: QueueWriteStream(queue_std_out),
        STREAM_CONFIG_KEY_QT_QUEUE_RECEIVER: StdOutTextQueueReceiver(q=queue_std_out)
    }
    perform_std_out_hack()


def perform_std_out_hack():
    sys.stdout = config_dict[STDOUT_WRITE_STREAM_CONFIG][STREAM_CONFIG_KEY_STREAM]


def configure_tqdm_redirection(tqdm_nb_columns=None):
    queue_tqdm = Queue()
    config_dict[TQDM_WRITE_STREAM_CONFIG] = {
        STREAM_CONFIG_KEY_QUEUE: queue_tqdm,
        STREAM_CONFIG_KEY_STREAM: QueueWriteStream(queue_tqdm),
        STREAM_CONFIG_KEY_QT_QUEUE_RECEIVER: TQDMTextQueueReceiver(q=queue_tqdm)
    }
    perform_tqdm_default_out_stream_hack(
        tqdm_file_stream=config_dict[TQDM_WRITE_STREAM_CONFIG][STREAM_CONFIG_KEY_STREAM],
        tqdm_nb_columns=tqdm_nb_columns)


class StdOutTextQueueReceiver(QObject):
    # we are forced to define 1 signal per class
    # see https://stackoverflow.com/questions/50294652/how-to-create-pyqtsignals-dynamically
    queue_std_out_element_received_signal = pyqtSignal(str)

    def __init__(self, q: Queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = q

    @pyqtSlot()
    def run(self):
        self.queue_std_out_element_received_signal.emit('---> STD OUT Queue reception Started <---\n')
        while True:
            text = self.queue.get()
            self.queue_std_out_element_received_signal.emit(text)


class TQDMTextQueueReceiver(QObject):
    # we are forced to define 1 signal per class
    # see https://stackoverflow.com/questions/50294652/how-to-create-pyqtsignals-dynamically
    queue_tqdm_element_received_signal = pyqtSignal(str)

    def __init__(self, q: Queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = q

    @pyqtSlot()
    def run(self):
        # we assume that all TQDM outputs start with \r, so use that to show stream reception is started
        self.queue_tqdm_element_received_signal.emit('\r---> TQDM Queue reception Started <---\n')
        while True:
            text = self.queue.get()
            self.queue_tqdm_element_received_signal.emit(text)

class StdOutTextEdit(QTextBrowser):
    def __init__(self, parent):
        super(QTextBrowser, self).__init__(parent)
        # self.setParent(parent)
        self.setReadOnly(True)
        # self.setLineWidth(50)
        # self.setMinimumWidth(500)
        # self.setFont(QFont('Consolas', 11))

    @pyqtSlot(str)
    def append_text(self, text: str):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)


class StdTQDMTextEdit(QLineEdit):
    def __init__(self, parent):
        super(StdTQDMTextEdit, self).__init__()
        self.setParent(parent)
        self.setReadOnly(True)
        self.setEnabled(True)
        # self.setMinimumWidth(500)
        # self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.setClearButtonEnabled(True)
        # self.setFont(QFont('Consolas', 11))

    @pyqtSlot(str)
    def set_tqdm_text(self, text: str):
        new_text = text
        if new_text.find('\r') >= 0:
            new_text = new_text.replace('\r', '').rstrip()
            if new_text:
                self.setText(new_text)
        else:
            # we suppose that all TQDM prints have \r, so drop the rest
            pass

class LongProcedureWrapper(QObject):
    def __init__(self, main_app):
        super(LongProcedureWrapper, self).__init__()
        self._main_app = main_app

    @pyqtSlot()
    def run(self):
        long_procedure()

def long_procedure():

    setup_logging('long_procedure')
    __logger = logging.getLogger('long_procedure')
    __logger.setLevel(logging.DEBUG)
    tqdm_obect = t_AUTO.tqdm(range(10), unit_scale=True, dynamic_ncols=True)
    tqdm_obect.set_description("My progress bar description")
    for i in tqdm_obect:
        time.sleep(.1)
        __logger.info('foo {}'.format(i))

setup_streams_redirection()