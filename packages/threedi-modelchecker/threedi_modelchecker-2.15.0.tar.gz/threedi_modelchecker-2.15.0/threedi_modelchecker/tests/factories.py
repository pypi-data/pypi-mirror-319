from inspect import isclass

import factory
from factory import Faker
from threedi_schema import constants, models


def inject_session(session):
    """Inject the session into all factories"""
    for _, cls in globals().items():
        if isclass(cls) and issubclass(cls, factory.alchemy.SQLAlchemyModelFactory):
            cls._meta.sqlalchemy_session = session


class TimeStepSettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.TimeStepSettings
        sqlalchemy_session = None

    time_step = 30
    min_time_step = 1
    max_time_step = 100
    output_time_step = 300
    use_time_step_stretch = False


class ModelSettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ModelSettings
        sqlalchemy_session = None

    friction_averaging = 0
    minimum_cell_size = 20
    calculation_point_distance_1d = 15
    minimum_table_step_size = 0.05
    use_1d_flow = False
    use_2d_rain = 1
    nr_grid_levels = 4
    friction_coefficient = 0.03
    use_2d_flow = True
    friction_type = constants.FrictionType.CHEZY


class ConnectionNodeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ConnectionNode
        sqlalchemy_session = None

    code = Faker("name")
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class ChannelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Channel
        sqlalchemy_session = None

    display_name = Faker("name")
    code = Faker("name")
    exchange_type = constants.CalculationType.CONNECTED
    geom = "SRID=4326;LINESTRING(-71.064544 42.28787, -71.0645 42.287)"


class WeirFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Weir
        sqlalchemy_session = None

    code = factory.Sequence(lambda n: "Code %d" % n)
    display_name = "display_name"
    crest_level = 1.0
    crest_type = constants.CrestType.BROAD_CRESTED
    friction_value = 2.0
    friction_type = constants.FrictionType.CHEZY
    sewerage = False
    connection_node_id_start = 1
    connection_node_id_end = 1
    geom = "SRID=4326;LINESTRING(4.885534714757985 52.38513158257129,4.88552805617346 52.38573773758626)"


class BoundaryConditions2DFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.BoundaryConditions2D
        sqlalchemy_session = None

    type = constants.BoundaryType.WATERLEVEL.value
    timeseries = "0,-0.5"
    display_name = Faker("name")
    geom = "SRID=4326;LINESTRING(4.885534714757985 52.38513158257129,4.88552805617346 52.38573773758626)"


class BoundaryConditions1DFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.BoundaryCondition1D
        sqlalchemy_session = None

    type = constants.BoundaryType.WATERLEVEL
    timeseries = "0,-0.5"
    connection_node_id = 1
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class PumpMapFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.PumpMap
        sqlalchemy_session = None

    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class PumpFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Pump
        sqlalchemy_session = None

    code = "code"
    display_name = "display_name"
    sewerage = False
    type_ = constants.PumpType.DELIVERY_SIDE
    start_level = 1.0
    lower_stop_level = 0.0
    capacity = 5.0
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class CrossSectionLocationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.CrossSectionLocation
        sqlalchemy_session = None

    code = "code"
    reference_level = 0.0
    friction_type = constants.FrictionType.CHEZY
    friction_value = 0.0
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class AggregationSettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.AggregationSettings
        sqlalchemy_session = None

    flow_variable = "waterlevel"
    aggregation_method = "avg"
    interval = 10


class NumericalSettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.NumericalSettings
        sqlalchemy_session = None

    max_degree_gauss_seidel = 1
    use_of_cg = 20
    use_nested_newton = 0
    flooding_threshold = 0.01


class Lateral1dFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Lateral1d
        sqlalchemy_session = None

    timeseries = "0,-0.1"
    connection_node_id = 1
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class Lateral2DFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Lateral2D
        sqlalchemy_session = None

    timeseries = "0,-0.2"
    geom = "SRID=4326;POINT(-71.064544 42.28787)"
    type = constants.Later2dType.SURFACE


class SurfaceParameterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.SurfaceParameter
        sqlalchemy_session = None

    outflow_delay = 10.0
    surface_layer_thickness = 5.0
    infiltration = True
    max_infiltration_capacity = 10.0
    min_infiltration_capacity = 5.0
    infiltration_decay_constant = 3.0
    infiltration_recovery_constant = 2.0


class DryWheatherFlowMapFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.DryWeatherFlowMap
        sqlalchemy_session = None

    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class DryWeatherFlowFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.DryWeatherFlow
        sqlalchemy_session = None

    geom = "SRID=4326;POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"


class DryWeatherFlowDistributionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.DryWeatherFlowDistribution
        sqlalchemy_session = None

    id = 1
    distribution = (
        "3,1.5,1,1,0.5,0.5,2.5,8,7.5,6,5.5,5,4.5,4,4,3.5,3.5,4,5.5,8,7,5.5,4.5,4"
    )


class SurfaceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Surface
        sqlalchemy_session = None

    area = 0.0
    geom = "SRID=4326;POLYGON((30 10, 40 40, 20 40, 10 20, 30 10))"

    # surface_parameters = factory.SubFactory(SurfaceParameterFactory)


class SurfaceMapFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.SurfaceMap
        sqlalchemy_session = None

    percentage = 100.0
    geom = "SRID=4326;LINESTRING(30 10, 10 30, 40 40)"


class TagsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Tags
        sqlalchemy_session = None


class ControlTableFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ControlTable
        sqlalchemy_session = None

    action_type = constants.ControlTableActionTypes.set_discharge_coefficients
    action_table = "0.0,-1.0 2.0\n1.0,-1.1 2.1"
    measure_operator = constants.MeasureOperators.greater_than
    target_type = constants.StructureControlTypes.channel
    target_id = 10
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class ControlMemoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ControlMemory
        sqlalchemy_session = None

    action_type = constants.ControlTableActionTypes.set_discharge_coefficients
    action_value_1 = 0.0
    action_value_2 = -1.0
    target_type = constants.StructureControlTypes.channel
    target_id = 10
    is_inverse = False
    is_active = True
    upper_threshold = 1.0
    lower_threshold = -1.0
    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class ControlMeasureMapFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ControlMeasureMap
        sqlalchemy_session = None

    control_type = constants.MeasureVariables.waterlevel
    geom = "SRID=4326;LINESTRING(30 10, 10 30, 40 40)"


class ControlMeasureLocationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ControlMeasureLocation
        sqlalchemy_session = None

    geom = "SRID=4326;POINT(-71.064544 42.28787)"


class CulvertFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Culvert
        sqlalchemy_session = None

    code = "code"
    display_name = Faker("name")
    exchange_type = constants.CalculationTypeCulvert.ISOLATED_NODE
    geom = "SRID=4326;LINESTRING(-71.064544 42.28787, -71.0645 42.287)"
    friction_value = 0.03
    friction_type = 2
    invert_level_start = 0.1
    invert_level_end = 1.1
    discharge_coefficient_negative = 1.0
    discharge_coefficient_positive = 1.0


class PotentialBreachFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.PotentialBreach
        sqlalchemy_session = None

    display_name = Faker("name")
    code = "code"
    geom = "SRID=4326;LINESTRING(-71.06452 42.2874, -71.06452 42.286)"


class VegetationDragFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.VegetationDrag
        sqlalchemy_session = None

    vegetation_height = 1.0
    vegetation_height_file = "vegetation_height_file.txt"

    vegetation_stem_count = 50000
    vegetation_stem_count_file = "vegetation_stem_count_file.txt"

    vegetation_stem_diameter = 0.5
    vegetation_stem_diameter_file = "vegetation_stem_diameter_file.txt"

    vegetation_drag_coefficient = 0.4
    vegetation_drag_coefficient_file = "vegetation_drag_coefficient_file.txt"


class SimulationTemplateSettingsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.SimulationTemplateSettings
        sqlalchemy_session = None

    name = "Foo"
    use_0d_inflow = constants.InflowType.NO_INFLOW
