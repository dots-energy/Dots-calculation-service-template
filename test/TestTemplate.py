from datetime import datetime
import unittest
from ExampleCalculationService.EConnection import CalculationServiceEConnection
from dots_infrastructure.DataClasses import SimulatorConfiguration
import helics as h

from dots_infrastructure import CalculationServiceHelperFunctions

BROKER_TEST_PORT = 23404
START_DATE_TIME = datetime(2024, 1, 1, 0, 0, 0)
SIMULATION_DURATION_IN_SECONDS = 960

def simulator_environment_e_connection():
    return SimulatorConfiguration("EConnection", ["f006d594-0743-4de5-a589-a6c2350898da"], "Mock-Econnection", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", h.HelicsLogLevel.DEBUG, ["PVInstallation", "EConnection"])

class Test(unittest.TestCase):

    def setUp(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection

    def test_empty_test(self):
        service = CalculationServiceEConnection()
        # Implement Test Logic here 
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()