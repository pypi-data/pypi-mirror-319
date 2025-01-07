import sys
from PyQt5.QtWidgets import QApplication
from spectral_sound_analysis import SpectrumAnalyzer


def main():
    """
    Main entry point for the script.
    """
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create and show the main GUI window
    analyzer = SpectrumAnalyzer()
    analyzer.show()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

