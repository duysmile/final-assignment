from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import ImageProcessing as ImgPro
import multiTextField as dialog
import CheckQualityImage as quality
from datetime import datetime
import About
from denoise_type import DenoiseType


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Denoise Poisson image'
        self.originalImagePath = None
        self.originalImage = None
        self.noiseType = None
        self.noiseImage = None
        self.resultImage = None
        self.timeRun = 0
        self.denoiseType = DenoiseType.poisson
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        central = QtWidgets.QWidget()
        self.mainView = QtWidgets.QGridLayout()
        central.setLayout(self.mainView)
        self.setCentralWidget(central)

        self.addMenuBar()
        self.addGroupAddNoiseButton()
        self.addGroupDenoiseButton()
        self.addGroupImage()
        self.addSaveImageButton()
        self.addResultDenoiseImage()
        self.addParameterView()

        imageView = QtWidgets.QGridLayout()
        imageView.addWidget(self.groupOriginalImage, 1, 0)
        imageView.addWidget(self.groupNoiseImage, 1, 1)
        imageView.addWidget(self.groupResultImage, 1, 2)
        self.mainView.addLayout(imageView, 2, 0)

        buttonGroup = QtWidgets.QGridLayout()
        buttonGroup.addWidget(self.addPoissonButon, 0, 0)
        buttonGroup.addWidget(self.groupDenoiseButton, 1, 0)
        buttonGroup.addWidget(self.groupParams, 2, 0)

        viewBottom = QtWidgets.QGridLayout()
        viewBottom.addLayout(buttonGroup, 1, 0)
        viewBottom.addWidget(self.groupResultDenoise, 1, 1)

        self.mainView.addLayout(viewBottom, 3, 0)

        btnGroup = QtWidgets.QGridLayout()

        runButton = QtWidgets.QPushButton(text="RUN")
        runButton.setStyleSheet(
            "font-weight: bold; color: black; font-size: 20; background-color: #FFFFFF")
        runButton.pressed.connect(self.clickRunButton)
        runButton.setFixedSize(300, 40)

        clearButton = QtWidgets.QPushButton(text="Clear")
        clearButton.setStyleSheet(
            "font-weight: bold; color: white; font-size: 20; background-color: red")
        clearButton.setFixedSize(300, 40)
        clearButton.pressed.connect(self.clearData)

        saveButton = QtWidgets.QPushButton(text="Save")
        saveButton.setStyleSheet(
            "font-weight: bold; color: white; font-size: 20; background-color: green")
        saveButton.pressed.connect(self.chooseFolderSaveImage)
        saveButton.setFixedSize(300, 40)

        btnGroup.addWidget(runButton, 1, 0)
        btnGroup.addWidget(clearButton, 1, 1)
        btnGroup.addWidget(saveButton, 1, 2)
        self.mainView.addLayout(btnGroup, 4, 0)

        self.show()

    def addGroupAddNoiseButton(self):
        self.viewAddNoiseButton = QtWidgets.QGridLayout()

        self.addPoissonButon = QtWidgets.QPushButton(text="Add Poisson Noise")
        self.addPoissonButon.pressed.connect(self.addPoissonNoise)
        self.addPoissonButon.setFixedWidth(210)

        self.addPoissonButon.setLayout(self.viewAddNoiseButton)

    def addResultDenoiseImage(self):
        self.viewResult = QtWidgets.QGridLayout()
        self.groupResultDenoise = QtWidgets.QGroupBox("Result")

        self.noiseTypeLabel = QtWidgets.QLabel()
        self.noiseTypeLabel.setText("Type: ")
        self.noiseTypeLabel.setStyleSheet("font-weight: bold; color: black")

        self.inforLabel = QtWidgets.QLabel()
        self.inforLabel.setText("Noise level: ")
        self.inforLabel.setStyleSheet("font-weight: bold; color: black")

        self.psnrLabel = QtWidgets.QLabel()
        self.psnrLabel.setStyleSheet("font-weight: bold; color: black")
        self.psnrLabel.setText("PSNR: ")

        self.ssimLabel = QtWidgets.QLabel()
        self.ssimLabel.setStyleSheet("font-weight: bold; color: black")
        self.ssimLabel.setText("SSIM: ")

        self.timeRunLabel = QtWidgets.QLabel()
        self.timeRunLabel.setStyleSheet("font-weight: bold; color: black")
        self.timeRunLabel.setText("Time Run: ")

        self.viewResult.addWidget(self.noiseTypeLabel, 1, 0)
        self.viewResult.addWidget(self.inforLabel, 2, 0)
        self.viewResult.addWidget(self.psnrLabel, 3, 0)
        self.viewResult.addWidget(self.ssimLabel, 4, 0)
        self.viewResult.addWidget(self.timeRunLabel, 5, 0)

        self.groupResultDenoise.setLayout(self.viewResult)
        self.groupResultDenoise.setFixedWidth(350)

    def addParameterView(self):
        self.viewParams = QtWidgets.QGridLayout()
        self.groupParams = QtWidgets.QGroupBox("Parameters")

        self.betaLabel = QtWidgets.QLabel()
        self.betaLabel.setStyleSheet("font-weight: bold; color: black")
        self.betaLabel.setText("Beta:")

        self.betaTextField = QtWidgets.QLineEdit()
        self.betaTextField.setText("0.8")
        self.betaTextField.setDisabled(True)

        self.gammaLabel = QtWidgets.QLabel()
        self.gammaLabel.setStyleSheet("font-weight: bold; color: black")
        self.gammaLabel.setText("Gamma:")

        self.gammaTextField = QtWidgets.QLineEdit()
        self.gammaTextField.setText("0.8")
        self.gammaTextField.setDisabled(True)

        self.ro1Label = QtWidgets.QLabel()
        self.ro1Label.setStyleSheet("font-weight: bold; color: black")
        self.ro1Label.setText("Ro1:")

        self.ro1TextField = QtWidgets.QLineEdit()
        self.ro1TextField.setText("80")
        self.ro1TextField.setDisabled(True)

        self.ro2Label = QtWidgets.QLabel()
        self.ro2Label.setStyleSheet("font-weight: bold; color: black")
        self.ro2Label.setText("Ro2:")

        self.ro2TextField = QtWidgets.QLineEdit()
        self.ro2TextField.setText("100")
        self.ro2TextField.setDisabled(True)

        self.ro3Label = QtWidgets.QLabel()
        self.ro3Label.setStyleSheet("font-weight: bold; color: black")
        self.ro3Label.setText("Ro3:")

        self.ro3TextField = QtWidgets.QLineEdit()
        self.ro3TextField.setText("100")
        self.ro3TextField.setDisabled(True)

        self.alfa1Label = QtWidgets.QLabel()
        self.alfa1Label.setStyleSheet("font-weight: bold; color: black")
        self.alfa1Label.setText("Alfa 1:")

        self.alfa1TextField = QtWidgets.QLineEdit()
        self.alfa1TextField.setText("0.1")
        self.alfa1TextField.setDisabled(True)

        self.alfa2Label = QtWidgets.QLabel()
        self.alfa2Label.setStyleSheet("font-weight: bold; color: black")
        self.alfa2Label.setText("Alfa 2:")

        self.alfa2TextField = QtWidgets.QLineEdit()
        self.alfa2TextField.setText("0.2")
        self.alfa2TextField.setDisabled(True)

        self.viewParams.addWidget(self.betaLabel, 1, 0)
        self.viewParams.addWidget(self.betaTextField, 2, 0)
        self.viewParams.addWidget(self.gammaLabel, 3, 0)
        self.viewParams.addWidget(self.gammaTextField, 4, 0)
        self.viewParams.addWidget(self.ro1Label, 5, 0)
        self.viewParams.addWidget(self.ro1TextField, 6, 0)
        self.viewParams.addWidget(self.ro2Label, 7, 0)
        self.viewParams.addWidget(self.ro2TextField, 8, 0)
        self.viewParams.addWidget(self.ro3Label, 9, 0)
        self.viewParams.addWidget(self.ro3TextField, 10, 0)
        self.viewParams.addWidget(self.alfa1Label, 11, 0)
        self.viewParams.addWidget(self.alfa1TextField, 12, 0)
        self.viewParams.addWidget(self.alfa2Label, 13, 0)
        self.viewParams.addWidget(self.alfa2TextField, 14, 0)

        self.groupParams.setLayout(self.viewParams)
        self.groupParams.setFixedHeight(400)
        self.groupParams.setFixedWidth(200)

    def addGroupDenoiseButton(self):
        self.viewContainDenoiseButton = QtWidgets.QGridLayout()

        self.groupDenoiseButton = QtWidgets.QGroupBox("Denoise")

        self.poissonButton = QtWidgets.QRadioButton("For Poisson")
        self.poissonButton.toggled.connect(self.toggleRadioButton)
        self.poissonButton.setFixedWidth(200)

        self.poissonMoButton = QtWidgets.QRadioButton("For Poisson Modified")
        self.poissonMoButton.toggled.connect(self.toggleRadioButton)
        self.poissonMoButton.setFixedWidth(200)

        self.splitBregman = QtWidgets.QRadioButton("Split bregman")
        self.splitBregman.toggled.connect(self.toggleRadioButton)
        self.splitBregman.setFixedWidth(200)

        self.tv1tv2Bregman = QtWidgets.QRadioButton("TV1TV2")
        self.tv1tv2Bregman.toggled.connect(self.toggleRadioButton)
        self.tv1tv2Bregman.setFixedWidth(200)

        self.viewContainDenoiseButton.addWidget(self.poissonButton, 1, 0)
        self.viewContainDenoiseButton.addWidget(self.poissonMoButton, 2, 0)
        self.viewContainDenoiseButton.addWidget(self.splitBregman, 3, 0)
        self.viewContainDenoiseButton.addWidget(self.tv1tv2Bregman, 4, 0)

        self.groupDenoiseButton.setLayout(self.viewContainDenoiseButton)
        self.groupDenoiseButton.setFixedHeight(100)
        self.groupDenoiseButton.setFixedWidth(200)

    def addGroupImage(self):
        self.groupOriginalImage = QtWidgets.QGroupBox("Original Image")

        self.originalImageView = QtWidgets.QLabel()
        self.originalImageView.setFixedSize(255, 255)

        originalImageLayout = QtWidgets.QGridLayout()
        originalImageLayout.addWidget(self.originalImageView)

        self.groupOriginalImage.setLayout(originalImageLayout)
        self.groupOriginalImage.setFixedHeight(300)

        self.groupNoiseImage = QtWidgets.QGroupBox("Noise Image")

        self.noiseImageView = QtWidgets.QLabel()
        self.noiseImageView.setFixedSize(255, 255)

        noiseImageLayout = QtWidgets.QGridLayout()
        noiseImageLayout.addWidget(self.noiseImageView)

        self.groupNoiseImage.setLayout(noiseImageLayout)
        self.groupNoiseImage.setFixedHeight(300)

        self.groupResultImage = QtWidgets.QGroupBox("Result Image")

        self.resultImageView = QtWidgets.QLabel()
        self.resultImageView.setFixedSize(255, 255)

        resultImageLayout = QtWidgets.QGridLayout()
        resultImageLayout.addWidget(self.resultImageView)

        self.groupResultImage.setLayout(resultImageLayout)
        self.groupResultImage.setFixedHeight(300)

    def addSaveImageButton(self):
        clearButton = QtWidgets.QPushButton(text="Clear")
        clearButton.setFixedWidth(150)
        clearButton.pressed.connect(self.clearData)

        saveButton = QtWidgets.QPushButton(text="Save")
        saveButton.pressed.connect(self.chooseFolderSaveImage)
        saveButton.setFixedWidth(150)

        self.viewClearSaveButton = QtWidgets.QHBoxLayout()
        self.viewClearSaveButton.addStretch()
        self.viewClearSaveButton.addWidget(clearButton)
        self.viewClearSaveButton.addWidget(saveButton)

    def addMenuBar(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        aboutMenu = mainMenu.addMenu('About')

        openButton = QtWidgets.QAction(
            QtGui.QIcon('exit24.png'), 'Open Image', self)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open an image')
        openButton.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction(openButton)

        aboutButton = QtWidgets.QAction(QtGui.QIcon(), 'About Project', self)
        aboutButton.triggered.connect(self.openAboutDialog)
        aboutMenu.addAction(aboutButton)

    @QtCore.pyqtSlot()
    def openAboutDialog(self):
        ui = About.Ui_Dialog()
        ui.setupUi()
        ui.exec_()

    @QtCore.pyqtSlot()
    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open image", "", "Image File (*.*)", options=options)
        if fileName:
            image = ImgPro.openImage(fileName)
            resizePath = ImgPro.saveImage("resizetemp.jpg", image)
            pixmap = QtGui.QPixmap(resizePath)
            self.clearData()
            self.originalImage = image
            self.originalImageView.setPixmap(pixmap)
            self.originalImagePath = resizePath

    @QtCore.pyqtSlot()
    def chooseFolderSaveImage(self):
        if self.resultImage is not None:
            result_im = ImgPro.rescale255(self.resultImage)

            noise_im = ImgPro.rescale255(self.noiseImage)

            options = QtWidgets.QFileDialog.Options()
            fileName_noise, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Noise image", "", "Image File (*.png *.jpg *.jpeg)", options=options)
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Result image", "", "Image File (*.png *.jpg *.jpeg)", options=options)
            if fileName_noise:
                ImgPro.customSaveImage(fileName_noise, noise_im)
            if fileName:
                ImgPro.customSaveImage(fileName, result_im)
                QtWidgets.QMessageBox.information(
                    self, "Image Processing", "Lưu ảnh thành công.")
        else:
            self.showAlert("Bạn chưa chọn ảnh nào.")

    @QtCore.pyqtSlot()
    def addPoissonNoise(self):
        if self.originalImagePath is not None:
            d, okPressed = QtWidgets.QInputDialog.getInt(
                self, "Enter value", "PEAK:", 120, 0, 255, 10)
            if okPressed:
                image = ImgPro.openImage(self.originalImagePath)
                image = ImgPro.addPossionNoise(image, peak=d)
                self.noiseType = "Poisson"
                self.setDenoiseData(image)
                self.inforLabel.setText(
                    "Noise level: PEAK = " + str(d) + ", SIGMA = " + str(0))
        else:
            self.showAlert("Bạn chưa chọn ảnh nào.")

    @QtCore.pyqtSlot()
    def toggleRadioButton(self):
        if self.poissonButton.isChecked():
            self.denoiseType = DenoiseType.poisson
            self.betaTextField.setText("0.8")
            self.setDisabledField(0, 1, 1, 1, 1, 1, 1)
        elif self.poissonMoButton.isChecked():
            self.denoiseType = DenoiseType.poissonModified
            self.betaTextField.setText("0.8")
            self.setDisabledField(0, 1, 1, 1, 1, 1, 1)
        elif self.splitBregman.isChecked():
            self.denoiseType = DenoiseType.splitBregman
            self.setDisabledField(0, 0, 0, 1, 1, 1, 1)
            self.ro1TextField.setText("80")
            self.ro2TextField.setText("100")
            self.betaTextField.setText("0.8")
        elif self.tv1tv2Bregman.isChecked():
            self.denoiseType = DenoiseType.splitBregmanTV1TV2
            self.gammaTextField.setText("18")
            self.ro1TextField.setText("2")
            self.ro2TextField.setText("2")
            self.ro3TextField.setText("1")
            self.alfa1TextField.setText("0.1")
            self.alfa2TextField.setText("0.1")
            self.betaTextField.setText("5")
            self.setDisabledField(0, 0, 0, 0, 1, 0, 0)

    def setDisabledField(self, beta, ro1, ro2, ro3, gamma, alfa1, alfa2):
        self.betaTextField.setDisabled(beta)
        self.ro1TextField.setDisabled(ro1)
        self.ro2TextField.setDisabled(ro2)
        self.ro3TextField.setDisabled(ro3)
        self.gammaTextField.setDisabled(gamma)
        self.alfa1TextField.setDisabled(alfa1)
        self.alfa2TextField.setDisabled(alfa2)

    def showAlert(self, message):
        QtWidgets.QMessageBox.warning(self, "Image Processing", message)

    @QtCore.pyqtSlot()
    def clickRunButton(self):
        if self.noiseImage is not None:
            beta = 0.8
            ro1 = 1
            ro2 = 1
            ro3 = 1
            gamma = 0.8
            alfa1 = 0.1
            alfa2 = 0.1

            if self.denoiseType == DenoiseType.poisson or self.denoiseType == DenoiseType.poissonModified:
                try:
                    beta = float(self.betaTextField.text())
                except ValueError:
                    self.showAlert("Vui lòng nhập hệ số beta")
                    return

            if self.denoiseType == DenoiseType.splitBregman or self.denoiseType == DenoiseType.splitBregmanTV1TV2:
                try:
                    beta = float(self.betaTextField.text())
                    ro1 = float(self.ro1TextField.text())
                    ro2 = float(self.ro2TextField.text())
                    ro3 = float(self.ro3TextField.text())
                    gamma = float(self.gammaTextField.text())
                    alfa1 = float(self.alfa1TextField.text())
                    alfa2 = float(self.alfa2TextField.text())
                except ValueError:
                    self.showAlert("Vui lòng nhập các hệ số")
                    return

            image = self.noiseImage
            start = datetime.now()
            if self.denoiseType == DenoiseType.poisson:
                image = ImgPro.tvDenoiseOnlyPoisson(image, beta=beta)
            elif self.denoiseType == DenoiseType.poissonModified:
                image = ImgPro.tvDenoiseOnlyPoissonModified(image, beta=beta)
            elif self.denoiseType == DenoiseType.splitBregmanTV1TV2:
                image = ImgPro.tvSecondOrder(
                    image, beta, ro1, ro2, ro3, alfa1, alfa2)
            else:
                image = ImgPro.tvBregman(
                    image, beta, ro1, ro2, gamma)

            self.timeRun = datetime.now() - start

            self.resultImage = image

            # rescale to [0..255]
            image = ImgPro.rescale255(image)
            resizePath = ImgPro.saveImage("denoiseResize.jpg", image)
            pixmap = QtGui.QPixmap(resizePath)
            self.resultImageView.setPixmap(pixmap)

            if self.originalImage is not None and self.resultImage is not None:
                self.evaluationImage(self.originalImage, self.resultImage)
        else:
            self.showAlert("Vui lòng chọn ảnh và thêm nhiễu vào ảnh.")

    @QtCore.pyqtSlot()
    def setDenoiseData(self, image):
        self.noiseImage = image

        im = self.originalImage
        self.originalImage = ImgPro.rescale1(im)

        resizePath = ImgPro.saveImage(
            "noiseResize.jpg", ImgPro.rescale255(image))
        pixmap = QtGui.QPixmap(resizePath)
        self.noiseImageView.setPixmap(pixmap)

        self.noiseTypeLabel.setText("Type: " + self.noiseType)
        self.clearWhenAddNoise()

    def clearData(self):
        self.resultImage = None
        self.originalImagePath = None
        self.noiseImage = None
        self.originalImageView.setPixmap(QtGui.QPixmap())
        self.noiseImageView.setPixmap(QtGui.QPixmap())
        self.resultImageView.setPixmap(QtGui.QPixmap())
        self.inforLabel.setText("Noise level: ")
        self.psnrLabel.setText("PSNR: ")
        self.ssimLabel.setText("SSIM: ")
        self.timeRunLabel.setText("Time Run: ")

    def clearWhenAddNoise(self):
        self.psnrLabel.setText("PSNR: ")
        self.ssimLabel.setText("SSIM: ")
        self.timeRunLabel.setText("Time Run: ")
        self.resultImageView.setPixmap(QtGui.QPixmap())

    def evaluationImage(self, original, denoised):
        psnr = quality.PSNR(original, denoised)
        ssim = quality.SSIM(original, denoised)
        self.psnrLabel.setText("PSNR: " + str(round(psnr, 4)))
        self.ssimLabel.setText("SSIM: " + str(round(ssim, 4)))
        self.timeRunLabel.setText(
            "Time Run: " + str(round(self.timeRun.total_seconds(), 4)))
