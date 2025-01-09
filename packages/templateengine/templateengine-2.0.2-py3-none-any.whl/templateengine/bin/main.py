import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from templateengine.container.TemplateEngineProcess import TemplateEngineProcess

if __name__ == "__main__":
    proc = TemplateEngineProcess()
    proc._config_path = "../config/config.yml"
    proc.run()
