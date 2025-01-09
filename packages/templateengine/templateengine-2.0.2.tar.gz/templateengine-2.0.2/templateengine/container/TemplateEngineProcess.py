from pip_services4_container import ProcessContainer
from ..build import TemplateEngineFactory, StrategiesFactory, PlannersFactory, ToolsFactory, AIModelsFactory, ExecutorsFactory

class TemplateEngineProcess(ProcessContainer):
    def __init__(self):
        super().__init__('templateengine-v2', 'Template engine process')

        self._factories.add(TemplateEngineFactory())
        self._factories.add(StrategiesFactory())
        self._factories.add(PlannersFactory())
        self._factories.add(ToolsFactory())
        self._factories.add(AIModelsFactory())
        self._factories.add(ExecutorsFactory())
