import os
import sys
from PIL import Image
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QProgressBar)
from PySide6.QtCore import QThreadPool, QRunnable, Signal, QObject

class WorkerSignals(QObject):
    progress = Signal(int)
    finished = Signal()

class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.signals.progress.emit(1)  # Emit progress update
        self.signals.finished.emit()  # Emit finished signal

class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_directory = None
        self.initUI()
        self.threadpool = QThreadPool()
        self.active_workers = 0

    def initUI(self):
        self.setWindowTitle('PNG to JPG Converter')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Select a directory and then run the conversion.")
        layout.addWidget(self.label)

        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)

        self.btn_choose_dir = QPushButton('Choose Directory', self)
        self.btn_choose_dir.clicked.connect(self.chooseDirectory)
        layout.addWidget(self.btn_choose_dir)

        self.btn_run_conversion = QPushButton('Run Conversion', self)
        self.btn_run_conversion.clicked.connect(self.runConversion)
        self.btn_run_conversion.setEnabled(False)  # Disable until a directory is chosen
        layout.addWidget(self.btn_run_conversion)

        self.setLayout(layout)

    def chooseDirectory(self):
        self.selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.selected_directory:
            self.label.setText(f"Selected Directory: {self.selected_directory}")
            self.btn_run_conversion.setEnabled(True)  # Enable the "Run" button after directory is selected

    def runConversion(self):
        if self.selected_directory:
            self.convertImages(self.selected_directory)

    def convertImages(self, directory):
        jpg_dir = os.path.join(directory, 'jpg')
        os.makedirs(jpg_dir, exist_ok=True)

        png_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
        total_files = len(png_files)
        self.progressBar.setMaximum(total_files)
        self.progressBar.setValue(0)
        self.active_workers = total_files

        if total_files == 0:
            self.label.setText("No PNG files found in the directory.")
            return

        for png_file in png_files:
            worker = Worker(self.convert_image, png_file, jpg_dir)
            worker.signals.progress.connect(self.updateProgress)
            worker.signals.finished.connect(self.checkAllFinished)
            self.threadpool.start(worker)

    def updateProgress(self, value):
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + value)

    def checkAllFinished(self):
        self.active_workers -= 1
        if self.active_workers == 0:
            self.label.setText("Conversion completed. All PNG files have been converted.")
            self.btn_run_conversion.setEnabled(False)  # Disable run button after conversion is done

    def convert_image(self, png_path, output_dir):
        try:
            img = Image.open(png_path)
            jpg_path = os.path.join(output_dir, os.path.splitext(os.path.basename(png_path))[0] + '.jpg')
            img.convert('RGB').save(jpg_path, 'JPEG')
        except Exception as e:
            print(f"Failed to convert {png_path}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = ImageConverter()
    converter.show()
    sys.exit(app.exec())


