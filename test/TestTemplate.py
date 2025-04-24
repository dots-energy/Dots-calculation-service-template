from datetime import datetime
import unittest
from ExampleCalculationService.CalculationServiceTest import CalculationServiceTest
from dots_infrastructure.DataClasses import SimulatorConfiguration, SimulaitonDataPoint, TimeStepInformation
from dots_infrastructure.test_infra.InfluxDBMock import InfluxDBMock
from esdl.esdl_handler import EnergySystemHandler
import helics as h

from dots_infrastructure import CalculationServiceHelperFunctions

BROKER_TEST_PORT = 23404
START_DATE_TIME = datetime(2024, 1, 1, 0, 0, 0)
SIMULATION_DURATION_IN_SECONDS = 960
TEST_ID = "test-id"

def simulator_environment_e_connection():
    return SimulatorConfiguration("EConnection", [TEST_ID], "Mock-Econnection", "127.0.0.1", BROKER_TEST_PORT, "test-id", SIMULATION_DURATION_IN_SECONDS, START_DATE_TIME, "test-host", "test-port", "test-username", "test-password", "test-database-name", h.HelicsLogLevel.DEBUG, ["PVInstallation", "EConnection"])

class Test(unittest.TestCase):

    def setUp(self):
        CalculationServiceHelperFunctions.get_simulator_configuration_from_environment = simulator_environment_e_connection
        esh = EnergySystemHandler()
        esh.load_file("test.esdl")
        self.energy_system = esh.get_energy_system()

    def test_example(self):
        # Arrange
        service = CalculationServiceTest()
        service.influx_connector = InfluxDBMock()
        pv_dispatch_params = {}
        pv_dispatch_params["input1"] = [1.0, 2.0]
        service.init_calculation_service(self.energy_system)

        # Execute
        ret_val = service.e_connection_dispatch(pv_dispatch_params, datetime(2024,1,1), TimeStepInformation(1,2), TEST_ID, self.energy_system)

        # Implement 
        self.assertEqual(ret_val["output1"], 3.0)
        self.assertListEqual([SimulaitonDataPoint("output1", datetime(2024,1,1), 3.0, TEST_ID)], service.influx_connector.data_points)

if __name__ == '__main__':
    unittest.main()
