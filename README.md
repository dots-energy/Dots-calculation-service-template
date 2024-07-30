# Dots Calculation service template
A template repository for DOTs-helics calculation services. 
To create a new calculation service follow the following steps (For a more detailed explenation see below):
1. Create a new github repository based on this template.
2. Edit the `EConnection.py` based upon your needs i.e. define the correct calculations for the calculation service.
3. Edit the `TestTemplate.py` to test your calculations indepedently in a python unit test
4. When everything works as expected use the `build_and_push_image_dockerhub.sh` script to push your image to dockerhub.

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
```

First, you can see a list called `subscriptions_values`. This list defines the inputs of the calculation. In this case it hase one input that is supposed to come from the ESDL type called `PVInstallation` as specified by the `esdl_type` parameter. Next, the `input_name` parameter describes the name of the value that the `PVInstallation` produces. Finally, the `input_unit` and `input_type` describe the input's unit and type respectively. 

The second list describes the publications or outputs of the calculation. There are two parameters of a publication description that are worth mentioning: `global_flag` this needs to be set to `True` and will be removed in later versions of this template, and, `esdl_type` this is the esdl type of the calculation service that you are defining in this case `EConnection`. 

After the definition of the subscription and publication values the actual calculation is defined by instantiating `HelicsCalculationInformation`. The first 5 parameters are related to a helics federate confguration and therefore the reader is reffered to the [helics documentation](https://docs.helics.org/en/latest/references/configuration_options_reference.html#broker_init_string--null). The other parameters should be self explenatory based their names. 

Finally, the the last line adds the calculation to the calculation service and ensures that it is executed during a running co-simulation. Every added calculation will become a [helics federate](https://docs.helics.org/en/latest/user-guide/fundamental_topics/helics_terminology.html) with their own timing parameters as defined in the `calculation_information`. To get an idea of how helics timing works have a look at this [page](https://docs.helics.org/en/latest/user-guide/fundamental_topics/timing_configuration.html) of the helics documentation.

## Testing a calculation service

1. Create a new python virtual environment
2. Install dependencies and package `pip install -e .`
3. Run `python -m unittest discover -s ./test -p 'Test*.py'`

## Building a docker image such that it can be used 

1. Adjust `<<ImageName>>` to the name of the calculation service's image in the file `.github/workflows/publish-image.yml`
2. Push your changes to a new branch
3. Create a pull request
4. A github action will now run building the calculation service as a docker image and pushing it to the registry, as long as the pull request is not merged in the main branch the version number will be `test`
5. When finished complete the pull request and a new docker image will be built and pushed with version number `latest`
