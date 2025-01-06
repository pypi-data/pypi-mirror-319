from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

#
#
#
from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical

light_source = SourceGeometrical(name='SourceGeometrical', nrays=5000, seed=5676561)
light_source.set_spatial_type_gaussian(sigma_h=0.000279, sigma_v=0.000015)
light_source.set_depth_distribution_off()
light_source.set_angular_distribution_gaussian(sigdix=0.000021, sigdiz=0.000018)
light_source.set_energy_distribution_singleline(1000.000000, unit='eV')
light_source.set_polarization(polarization_degree=1.000000, phase_diff=0.000000, coherent_beam=0)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
boundary_shape = None

from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirror

optical_element = S4PlaneMirror(name='Plane Mirror', boundary_shape=boundary_shape,
                                f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                coating_material='Si', coating_density=2.33, coating_roughness=0)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=28, q=0, angle_radial=1.544616388, angle_azimuthal=1.570796327,
                                 angle_radial_out=1.544616388)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirrorElement

beamline_element = S4PlaneMirrorElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                        input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
boundary_shape = None

from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirror

optical_element = S4PlaneMirror(name='Plane Mirror', boundary_shape=boundary_shape,
                                f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                coating_material='Si', coating_density=2.33, coating_roughness=0)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=1.779953, q=0.11035115, angle_radial=1.532244796, angle_azimuthal=4.71238898,
                                 angle_radial_out=1.532244796)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_plane_mirror import S4PlaneMirrorElement

beamline_element = S4PlaneMirrorElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                        input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
boundary_shape = None
from shadow4.beamline.optical_elements.gratings.s4_plane_grating import S4PlaneGrating

optical_element = S4PlaneGrating(name='Plane Grating',
                                 boundary_shape=None, f_ruling=1, order=-1,
                                 ruling=800000.0, ruling_coeff_linear=230792.0,
                                 ruling_coeff_quadratic=30998.4, ruling_coeff_cubic=0.0,
                                 ruling_coeff_quartic=0.0,
                                 )
from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=0.11035115, q=10, angle_radial=1.545112585, angle_azimuthal=3.141592654,
                                 angle_radial_out=1.519377007)
movements = None
from shadow4.beamline.optical_elements.gratings.s4_plane_grating import S4PlaneGratingElement

beamline_element = S4PlaneGratingElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                         input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
                 plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')