# -*- coding: utf-8 -*-
from datetime import datetime
from esdl import esdl
import helics as h
from dots_infrastructure.DataClasses import (
    EsdlId,
    HelicsCalculationInformation,
    PublicationDescription,
    SubscriptionDescription,
    TimeStepInformation,
    TimeRequestType,
)
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor
from dots_infrastructure.CalculationServiceHelperFunctions import (
    get_single_param_with_name,
    get_vector_param_with_name,
)
from dots_infrastructure.Logger import LOGGER
from esdl import EnergySystem


class ServiceBCalculation(HelicsSimulationExecutor):

    def __init__(self):
        super().__init__()

        subscriptions_values = [
            SubscriptionDescription(
                esdl_type="EConnection",
                input_name="Schedule",
                input_unit="W",
                input_type= h.HelicsDataType.VECTOR,
            )
        ]

        publication_values = [
            PublicationDescription(
                global_flag=True,
                esdl_type="PVInstallation",
                output_name="PV_Dispatch",
                output_unit="W",
                data_type=h.HelicsDataType.DOUBLE,
            )
        ]

        e_connection_period_in_seconds = 60

        calculation_information = HelicsCalculationInformation(
            time_period_in_seconds=e_connection_period_in_seconds,
            offset=0,
            uninterruptible=False,
            wait_for_current_time_update=False,
            terminate_on_error=True,
            calculation_name="EConnectionDispatch",
            inputs=subscriptions_values,
            outputs=publication_values,
            calculation_function=self.pv_dispatch,
        )
        self.add_calculation(calculation_information)

    def init_calculation_service(self, energy_system: esdl.EnergySystem):
        LOGGER.info("init calculation service")
        for esdl_id in self.simulator_configuration.esdl_ids:
            LOGGER.info(f"Example of iterating over esdl ids: {esdl_id}")

    def pv_dispatch(
        self,
        param_dict: dict,
        simulation_time: datetime,
        time_step_number: TimeStepInformation,
        esdl_id: EsdlId,
        energy_system: EnergySystem,
    ):
        ret_val = {}
        single_dispatch_value = get_single_param_with_name(
            param_dict, "Schedule"
        )
        all_dispatch_values = get_vector_param_with_name(
            param_dict, "Schedule"
        )
        ret_val["PV_Dispatch"] = max(single_dispatch_value) / 2
        self.influx_connector.set_time_step_data_point(
            esdl_id,
            "PV_Dispatch",
            simulation_time,
            ret_val["PV_Dispatch"],
        )
        return ret_val


if __name__ == "__main__":
    helics_simulation_executor = ServiceBCalculation()
    helics_simulation_executor.start_simulation()
    helics_simulation_executor.stop_simulation()
