# coding=utf-8

import datetime
import logging
import sys
import time
from queue import Queue

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread, Qt
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QTextEdit, QWidget, QToolButton, QVBoxLayout, QApplication, QLineEdit


# DEFINITION NEEDED FIRST ...
class WriteStream(object):
    def __init__(self, q: Queue):
        self.queue = q

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass


# prepare queue and streams
queue_tqdm = Queue()
write_stream_tqdm = WriteStream(queue_tqdm)

################## START TQDM patch procedure ##################
import tqdm

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
                                        write_stream_tqdm,  # change any chosen file stream with our's
                                        80,  # change nb of columns (gui choice),
                                        mininterval, maxinterval,
                                        miniters, ascii, disable, unit,
                                        unit_scale, False, smoothing,
                                        bar_format, initial, position, postfix,
                                        unit_divisor, gui, **kwargs)
        print('TQDM Patch called') # check it works

    @classmethod
    def write(cls, s, file=None, end="\n", nolock=False):
        super(TQDMPatch, cls).write(s=s, file=file, end=end, nolock=nolock)

    # all other tqdm.orignal_class @classmethod methods may need to be redefined !


# I mainly used tqdm.auto in my modules, so use that for patch
# unsure if this will work with all possible tqdm import methods
# might not work for tqdm_gui !
import tqdm.auto as AUTO

# change original class with the patched one, the original still exists
AUTO.tqdm = TQDMPatch
################## END of TQDM patch ##################

# normal MCVE code
__is_setup_done = False


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        setup_logging(self.__class__.__name__)

        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__logger.setLevel(logging.DEBUG)

        # create stdout text queue
        self.queue_std_out = Queue()
        sys.stdout = WriteStream(self.queue_std_out)

        layout = QVBoxLayout()

        self.setMinimumWidth(500)

        self.btn_perform_actions = QToolButton(self)
        self.btn_perform_actions.setText('Launch long processing')
        self.btn_perform_actions.clicked.connect(self._btn_go_clicked)

        self.text_edit_std_out = StdOutTextEdit(self)
        self.text_edit_tqdm = StdTQDMTextEdit(self)

        self.thread_initialize = QThread()
        self.init_procedure_object = InitializationProcedures(self)

        # std out stream management
        # create console text read thread + receiver object
        self.thread_std_out_queue_listener = QThread()
        self.std_out_text_receiver = ThreadStdOutStreamTextQueueReceiver(self.queue_std_out)
        # connect receiver object to widget for text update
        self.std_out_text_receiver.queue_std_out_element_received_signal.connect(self.text_edit_std_out.append_text)
        # attach console text receiver to console text thread
        self.std_out_text_receiver.moveToThread(self.thread_std_out_queue_listener)
        # attach to start / stop methods
        self.thread_std_out_queue_listener.started.connect(self.std_out_text_receiver.run)
        self.thread_std_out_queue_listener.start()

        # NEW: TQDM stream management
        self.thread_tqdm_queue_listener = QThread()
        self.tqdm_text_receiver = ThreadTQDMStreamTextQueueReceiver(queue_tqdm)
        # connect receiver object to widget for text update
        self.tqdm_text_receiver.queue_tqdm_element_received_signal.connect(self.text_edit_tqdm.set_tqdm_text)
        # attach console text receiver to console text thread
        self.tqdm_text_receiver.moveToThread(self.thread_tqdm_queue_listener)
        # attach to start / stop methods
        self.thread_tqdm_queue_listener.started.connect(self.tqdm_text_receiver.run)
        self.thread_tqdm_queue_listener.start()

        layout.addWidget(self.btn_perform_actions)
        layout.addWidget(self.text_edit_std_out)
        layout.addWidget(self.text_edit_tqdm)
        self.setLayout(layout)
        self.show()

    @pyqtSlot()
    def _btn_go_clicked(self):
        # prepare thread for long operation
        self.init_procedure_object.moveToThread(self.thread_initialize)
        self.thread_initialize.started.connect(self.init_procedure_object.run)
        self.thread_initialize.finished.connect(self.init_procedure_object.finished)
        # start thread
        self.btn_perform_actions.setEnabled(False)
        self.thread_initialize.start()


class ThreadStdOutStreamTextQueueReceiver(QObject):
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


# NEW: dedicated receiving object for TQDM
class ThreadTQDMStreamTextQueueReceiver(QObject):
    queue_tqdm_element_received_signal = pyqtSignal(str)

    def __init__(self, q: Queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = q

    @pyqtSlot()
    def run(self):
        self.queue_tqdm_element_received_signal.emit('\r---> TQDM Queue reception Started <---\n')
        while True:
            text = self.queue.get()
            self.queue_tqdm_element_received_signal.emit(text)


class StdOutTextEdit(QTextEdit):  # QTextEdit):
    def __init__(self, parent):
        super(StdOutTextEdit, self).__init__()
        self.setParent(parent)
        self.setReadOnly(True)
        self.setLineWidth(50)
        self.setMinimumWidth(500)
        self.setFont(QFont('Consolas', 11))

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
        self.setMinimumWidth(500)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setClearButtonEnabled(True)
        self.setFont(QFont('Consolas', 11))

    @pyqtSlot(str)
    def set_tqdm_text(self, text: str):
        new_text = text
        if new_text.find('\r') >= 0:
            new_text = new_text.replace('\r', '').rstrip()
            if new_text:
                self.setText(new_text)
        else:
            # we suppose that all TQDM prints have \r
            # so drop the rest
            pass


def long_procedure():
    # emulate import of modules
    from tqdm.auto import tqdm

    setup_logging('long_procedure')
    __logger = logging.getLogger('long_procedure')
    __logger.setLevel(logging.DEBUG)
    tqdm_obect = tqdm(range(10), unit_scale=True, dynamic_ncols=True)
    tqdm_obect.set_description("My progress bar description")
    for i in tqdm_obect:
        time.sleep(.1)
        __logger.info('foo {}'.format(i))


class InitializationProcedures(QObject):
    def __init__(self, main_app: MainApp):
        super(InitializationProcedures, self).__init__()
        self._main_app = main_app

    @pyqtSlot()
    def run(self):
        long_procedure()

    @pyqtSlot()
    def finished(self):
        print("Thread finished !")  # might call main window to do some stuff with buttons
        self._main_app.btn_perform_actions.setEnabled(True)


def setup_logging(log_prefix):
    global __is_setup_done

    if __is_setup_done:
        pass
    else:
        __log_file_name = "{}-{}_log_file.txt".format(log_prefix,
                                                      datetime.datetime.utcnow().isoformat().replace(":", "-"))

        __log_format = '%(asctime)s - %(name)-30s - %(levelname)s - %(message)s'
        __console_date_format = '%Y-%m-%d %H:%M:%S'
        __file_date_format = '%Y-%m-%d %H-%M-%S'

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        console_formatter = logging.Formatter(__log_format, __console_date_format)

        file_formatter = logging.Formatter(__log_format, __file_date_format)
        file_handler = logging.FileHandler(__log_file_name, mode='a', delay=True)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        root.addHandler(file_handler)

        tqdm_handler = TqdmLoggingHandler()
        tqdm_handler.setLevel(logging.DEBUG)
        tqdm_handler.setFormatter(console_formatter)
        root.addHandler(tqdm_handler)

        __is_setup_done = True


class TqdmLoggingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        tqdm.tqdm.write(msg)
        # from https://stackoverflow.com/questions/38543506/change-logging-print-function-to-tqdm-write-so-logging-doesnt-interfere-wit/38739634#38739634
        self.flush()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainApp()
    sys.exit(app.exec_())