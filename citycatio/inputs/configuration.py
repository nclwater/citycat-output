import os
import xml.etree.cElementTree as ET
# noinspection PyUnresolvedReferences
from xml.dom import minidom


class Configuration:
    """General configuration options and infiltration parameters

    Args:
        duration: Length of simulation in seconds
        rainfall_zones: Number of rainfall zones
        permeable_areas_friction: Friction coefficient for permeable areas
        impermeable_areas_friction: Friction coefficient for impermeable areas
        spatial_rainfall: Whether or not rainfall is spatially variable
        output_interval: Time in seconds between output files
        initial_timestep: Time in seconds between first and second model time steps
        use_infiltration: Whether or not to include infiltration
        hydraulic_conductivity: Hydraulic conductivity of green areas
        wetting_front_suction_head: Wetting front suction head of green areas
        effective_porosity: Effective porosity of green areas
        effective_saturation: Effective saturation of green areas
        roof_storage: Roof storage of buildings in metres
    """
    def __init__(
            self,
            duration: int,
            rainfall_zones: int,
            permeable_areas_friction: float = 0.035,
            impermeable_areas_friction: float = 0.02,
            spatial_rainfall: bool = False,
            output_interval: int = 30 * 3600,
            initial_timestep: int = 25,
            use_infiltration: bool = False,
            hydraulic_conductivity: float = 1.09,
            wetting_front_suction_head: float = 11.01,
            effective_porosity: float = 0.412,
            effective_saturation: float = 0.3,
            roof_storage: float = 0
    ):
        self.duration = duration
        self.rainfall_zones = rainfall_zones
        self.permeable_areas_friction = permeable_areas_friction
        self.impermeable_areas_friction = impermeable_areas_friction
        self.spatial_rainfall = spatial_rainfall
        self.output_interval = output_interval
        self.initial_timestep = initial_timestep
        self.use_infiltration = use_infiltration
        self.hydraulic_conductivity = hydraulic_conductivity
        self.wetting_front_suction_head = wetting_front_suction_head
        self.effective_porosity = effective_porosity
        self.effective_saturation = effective_saturation
        self.roof_storage = roof_storage

    def write(self, path):

        config = ET.Element('CityCatConfiguration')

        num_scheme = ET.SubElement(config, 'NumericalScheme')
        scheme = ET.SubElement(num_scheme, 'Scheme')
        scheme.text = '6'

        flux_limiter = ET.SubElement(num_scheme, 'FluxLimiterFunction')
        flux_limiter.text = '1'
        slope_limiter = ET.SubElement(num_scheme, 'SlopeLimiterFunction')
        slope_limiter.text = '4'

        run_time = ET.SubElement(config, 'SimulationRunTime')
        run_time.set('units', 'secs')
        run_time.text = str(self.duration)

        results_step = ET.SubElement(config, 'OutputFrequency')
        results_step.set('units', 'secs')
        results_step.text = str(self.output_interval)

        initial_dt = ET.SubElement(config, 'InitialDt')
        initial_dt.set('units', 'secs')
        initial_dt.text = str(self.initial_timestep)

        rainfall = ET.SubElement(config, 'RainfallData')
        rainfall.set('spatial', str(self.spatial_rainfall))
        rainfall.set('zones', str(self.rainfall_zones))

        roof_storage = ET.SubElement(config, 'RoofStorage')
        roof_storage.set('units', 'meters')
        roof_storage.text = str(self.roof_storage)

        friction_coeffs = ET.SubElement(config, 'FrictionCoefficients')
        impermeable = ET.SubElement(friction_coeffs, 'CoeffForImpermeableAreas')
        impermeable.text = str(self.impermeable_areas_friction)
        permeable = ET.SubElement(friction_coeffs, 'CoeffForPermeableAreas')
        permeable.text = str(self.permeable_areas_friction)

        infiltration = ET.SubElement(config, 'Infiltration')
        infiltration.set('model', 'GreenAmpt')
        infiltration.set('useInfitration', str(self.use_infiltration))
        params = ET.SubElement(infiltration, 'InfiltrationParams')
        params.set('soilId', '1')
        conductivity = ET.SubElement(params, 'HydrConductivity')
        conductivity.set('units', 'cm/hr')
        conductivity.text = str(self.hydraulic_conductivity)
        suction = ET.SubElement(params, 'WettingFrontSuctionHead')
        suction.set('units', 'cm')
        suction.text = str(self.wetting_front_suction_head)
        porosity = ET.SubElement(params, 'EffectivePorosity')
        porosity.text = str(self.effective_porosity)
        saturation = ET.SubElement(params, 'EffectiveSaturation')
        saturation.text = str(self.effective_saturation)

        # 0 means use the Spatial_GreenAreas.txt file, 1 means all impermeable and 2 means all permeable
        permeable_areas = ET.SubElement(config, 'PermeableAreas')
        permeable_areas.text = '0'

        initial_conditions = ET.SubElement(config, 'InitSurfaceWaterElevation')
        initial_conditions.set('set', 'False')
        initial_conditions.set('spatial', 'False')
        initial_conditions.text = '0.00'

        max_depth = ET.SubElement(config, 'CreateMaxDepthFile')
        max_depth.set('fileformat', 'csv')
        max_depth.text = 'False'

        subsurface = ET.SubElement(config, 'SubsurfaceNetwork')
        subsurface.set('useNetworkModel', 'False')
        max_dx = ET.SubElement(subsurface, 'MaxDx')
        max_dx.set('units', 'meters')
        max_dx.text = '0.50'
        save_discharge = ET.SubElement(subsurface, 'SaveDischarge')
        save_discharge.text = 'False'

        with open(os.path.join(path, 'CityCat_Config_1.txt'), 'w') as f:

            f.write(minidom.parseString(ET.tostring(config, )).toprettyxml(indent='\t'))
