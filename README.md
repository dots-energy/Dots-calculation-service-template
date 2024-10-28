# Dots Calculation service template
A template repository for DOTs-helics calculation services. 
To create a new calculation service follow the following steps (For a more detailed explenation see below):
1. Create a new github repository based on this template.
2. Edit the `EConnection.py` based upon your needs i.e. define the correct calculations for the calculation service.
3. Edit the `TestTemplate.py` to test your calculations indepedently in a python unit test.
4. Replace the placeholders in the `Dockerfile`. The foldername should match the one that is in the src folder.

## Creating a calculation in the calculation service
The initial `EConnection.py` defines two calculations inside the `EConnection` calculation service. These calculations are called `EConnectionDispatch` and `EConnectionSchedule` respectively. Let's take a look at the definition of the first calculation:

```python
class CalculationServiceEConnection(HelicsSimulationExecutor):

    def __init__(self):
        super().__init__()

        subscriptions_values = [
            SubscriptionDescription(esdl_type="PVInstallation", 
                                    input_name="PV_Dispatch", 
                                    input_unit="W", 
                                    input_type=h.HelicsDataType.DOUBLE)
        ]

        publication_values = [
            PublicationDescription(global_flag=True, 
                                   esdl_type="EConnection", 
                                   output_name="EConnectionDispatch", 
                                   output_unit="W", 
                                   data_type=h.HelicsDataType.DOUBLE)
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
            calculation_function=self.e_connection_dispatch
        )
        self.add_calculation(calculation_information)

        publication_values = [
            PublicationDescription(True, "EConnection", "Schedule", "W", h.HelicsDataType.VECTOR)
        ]

        e_connection_period_in_seconds = 21600

        calculation_information_schedule = HelicsCalculationInformation(e_connection_period_in_seconds, TimeRequestType.PERIOD, 0, False, False, True, "EConnectionSchedule", [], publication_values, self.e_connection_da_schedule)
        self.add_calculation(calculation_information_schedule)

    def init_calculation_service(self, energy_system: esdl.EnergySystem):
        LOGGER.info("init calculation service")
        for esdl_id in self.simulator_configuration.esdl_ids:
            LOGGER.info(f"Example of iterating over esdl ids: {esdl_id}")

    def e_connection_dispatch(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        single_dispatch_value = get_single_param_with_name(param_dict, "PV_Dispatch") # returns the first value in param dict with "PV_Dispatch" in the key name
        all_dispatch_values = get_vector_param_with_name(param_dict, "PV_Dispatch") # returns all the values as a list in param_dict with "PV_Dispatch" in the key name
        ret_val["EConnectionDispatch"] = sum(single_dispatch_value)
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val["EConnectionDispatch"])
        return ret_val
```

First, you can see a list called `subscriptions_values`. This list defines the inputs of the calculation. In this case it hase one input that is supposed to come from the ESDL type called `PVInstallation` as specified by the `esdl_type` parameter. Next, the `input_name` parameter describes the name of the value that the `PVInstallation` produces. Finally, the `input_unit` and `input_type` describe the input's unit and type respectively. 

The second list describes the publications or outputs of the calculation. There are two parameters of a publication description that are worth mentioning: `global_flag` this needs to be set to `True` and will be removed in later versions of this template, and, `esdl_type` this is the esdl type of the calculation service that you are defining in this case `EConnection`. 

After the definition of the subscription and publication values the actual calculation is defined by instantiating `HelicsCalculationInformation`. The first 5 parameters are related to a helics federate confguration and therefore the reader is reffered to the [helics documentation](https://docs.helics.org/en/latest/references/configuration_options_reference.html#broker_init_string--null).

Finally, the the last line adds the calculation to the calculation service and ensures that it is executed during a running co-simulation. Every added calculation will become a [helics federate](https://docs.helics.org/en/latest/user-guide/fundamental_topics/helics_terminology.html) with their own timing parameters as defined in the `calculation_information`. To get an idea of how helics timing works have a look at this [page](https://docs.helics.org/en/latest/user-guide/fundamental_topics/timing_configuration.html) of the helics documentation.

When the simulation starts there will be an initialization stage and a calculating stage. In the initialization phase a calculation service can initialize variables that are required in the calculation stage. This can be done by adjusting the `init_calculation_service` function. The esdl that is associated with the simulated scenario is given as a parameter to this function.

In the calculation phase the calculation functions are called periodically for each simulated esdl entity. The `esdl_id` of the simulated entity is passed as a parameter to the calculation function. New inputs can be read and new outputs can be generated. An example of getting inputs, returning outputs and writing to the influx db can be found in the example above.

## Getting inputs from a calculation service
The input parameters provided by other calculation services are provided by the `param_dict` parameter in the calculation. Wheneve the calculation function `e_connection_dispatch` is called, the param dict for the calculation `e_connection_dispatch` could look like:

```
param_dict = {
    "PVInstallation/PV_Dispatch/1f60ceb9-9708-4d89-b079-482abc1408ea" : 5,
    "PVInstallation/PV_Dispatch/468f4332-4306-4b74-a5c2-eb8a7aa0a8d9" : 3,
}
```

This would mean that the associated esdl entity is connected to two `PVInstallation` entities with id `1f60ceb9-9708-4d89-b079-482abc1408ea` and `468f4332-4306-4b74-a5c2-eb8a7aa0a8d9` respectively. There are two ways to retrieve the values from the dictionary. First, by the python way of retrieving values from a dictiononary i.e. `param_dict[key]` this would require know the keys of dictionary. 
The second option is to use the helper functions in `dots_infrastructure.CalculationServiceHelperFunctions` (as shown in the above example). The function `get_single_param_with_name` will get the first value in `param_dict` with a specific input name. In the above example the input called `PV_Dispatch` is fetched and thus the function will return the vaule `5`. The other function to help retrieve values is called `get_vector_param_with_name` and will return all the values with a specific `input_name` as list. In this example it wil return the list `[5, 3]`.

## Testing a calculation service

1. Create a new python virtual environment
2. Install dependencies `pip install -r requirements.txt`
3. Install package `pip install -e .`
4. Run `python -m unittest discover -s ./test -p 'Test*.py'`

## Building a docker image such that it can be used 

1. Adjust `<<ImageName>>` to the name of the calculation service's image in the file `.github/workflows/publish-image.yml`
2. Push your changes to a new branch
3. Create a pull request
4. A github action will now run building the calculation service as a docker image and pushing it to the registry, as long as the pull request is not merged in the main branch the version number will be `test`
5. When finished complete the pull request and a new docker image will be built and pushed with version number `latest`
6. Change the visibility of the package to public, follow the steps detail [here](https://docs.github.com/en/enterprise-server@3.12/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#configuring-visibility-of-packages-for-an-organization).
