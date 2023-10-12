from PyQt5.QtGui import QFontDatabase, QFont


class FontType:
    def __init__(self):
        self.Font = None
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Black.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Bold.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Light.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Medium.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Regular.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Semibold.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Thin.otf")
        QFontDatabase.addApplicationFont("font/SF-Pro-Display-Ultralight.otf")
        self.font_db = QFontDatabase()

    def black(self, size=10):
        weight_Black = self.font_db.weight("SF Pro Display", "Black")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Black)
        return self.Font

    def bold(self, size=10):
        weight_Bold = self.font_db.weight("SF Pro Display", "Bold")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Bold)
        return self.Font

    def light(self, size=10):
        weight_Light = self.font_db.weight("SF Pro Display", "Light")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Light)
        return self.Font

    def medium(self, size=10):
        weight_Medium = self.font_db.weight("SF Pro Display", "Medium")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Medium)
        return self.Font

    def regular(self, size=10):
        weight_Regular = self.font_db.weight("SF Pro Display", "Regular")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Regular)
        return self.Font

    def semibold(self, size=10):
        weight_Semibold = self.font_db.weight("SF Pro Display", "Semibold")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Semibold)
        return self.Font

    def thin(self, size=10):
        weight_Thin = self.font_db.weight("SF Pro Display", "Thin")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Thin)
        return self.Font

    def ultralight(self, size=10):
        weight_Ultralight = self.font_db.weight("SF Pro Display", "Ultralight")
        self.Font = QFont("SF Pro Display", size)
        self.Font.setWeight(weight_Ultralight)
        return self.Font
