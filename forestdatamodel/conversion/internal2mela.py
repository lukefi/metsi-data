from copy import copy
from forestdatamodel.enums.mela import MelaTreeSpecies
from forestdatamodel.enums.internal import TreeSpecies
from forestdatamodel.conversion.util import apply_mappers

# TODO: can we find a way to resolve the circular import introduced by trying to use these classes just for typing?
# Even using the iffing below, pytest fails during top_level_collect
# if typing.TYPE_CHECKING:
#    from forestdatamodel.model import ForestStand, TreeStratum, ReferenceTree


species_map = {
    TreeSpecies.PINE: MelaTreeSpecies.SCOTS_PINE,
    TreeSpecies.SPRUCE: MelaTreeSpecies.NORWAY_SPRUCE,
    TreeSpecies.SILVER_BIRCH: MelaTreeSpecies.SILVER_BIRCH,
    TreeSpecies.DOWNY_BIRCH: MelaTreeSpecies.DOWNY_BIRCH,
    TreeSpecies.ASPEN: MelaTreeSpecies.ASPEN,
    TreeSpecies.GREY_ALDER: MelaTreeSpecies.ALDER,
    TreeSpecies.COMMON_ALDER: MelaTreeSpecies.ALDER,
    TreeSpecies.OTHER_CONIFEROUS: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.OTHER_DECIDUOUS: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.DOUGLAS_FIR: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.JUNIPER: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.SHORE_PINE: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.EUROPEAN_WHITE_ELM: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.LARCH: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.SMALL_LEAVED_LIME: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.BLACK_SPRUCE: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.WILLOW: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.MOUNTAIN_ASH: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.ABIES: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.GOAT_WILLOW: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.COMMON_ASH: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.KEDAR: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.SERBIAN_SPRUCE: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.OAK: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.BIRD_CHERRY: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.MAPLE: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.CURLY_BIRCH: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.WYCH_ELM: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.UNKNOWN_CONIFEROUS: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.UNKNOWN_DECIDUOUS: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.OTHER_PINE: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.OTHER_SPRUCE: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.THUJA: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.YEW: MelaTreeSpecies.OTHER_CONIFEROUS,
    TreeSpecies.BAY_WILLOW: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.POPLAR: MelaTreeSpecies.OTHER_DECIDUOUS,
    TreeSpecies.HAZEL: MelaTreeSpecies.OTHER_DECIDUOUS
}


def species_mapper(target):
    """in-place mapping from internal tree species to mela tree species"""
    target.species = species_map.get(target.species, MelaTreeSpecies.OTHER_DECIDUOUS)
    return target


def stand_location_converter(target):
    """
    in-place conversion of ForestStand geolocation to kilometer precision,
    and to YKJ/KKJ3 with band prefix 3 removed for EPSG:2393
    """
    if target.geo_location[3] == 'EPSG:3067':
        lat, lon = (target.geo_location[0] / 1000, target.geo_location[1] / 1000)
    elif target.geo_location[3] == 'EPSG:2393':
        lat, lon = (target.geo_location[0] / 1000, target.geo_location[1] / 1000 - 3000)
    else:
        raise Exception("Unsupported CRS {} for stand {}".format(target.geo_location[3], target.identifier))

    target.geo_location = (
        lat,
        lon,
        target.geo_location[2],
        target.geo_location[3])
    return target


def stand_area_converter(target):
    """ in-place conversion to for variables area and area weight when stands is auxiliary """
    if target.is_auxiliary():
        target.area_weight = target.area
        target.area = 0.0
    return target


def mela_stratum(stratum):
    """Convert a TreeStratum so that enumerated category variables are converted to Mela value space"""
    result = copy(stratum)
    result.stand_origin_relative_position = copy(stratum.stand_origin_relative_position)
    return apply_mappers(result, *default_mela_stratum_mappers)


def mela_tree(tree):
    """Convert a ReferenceTree so that enumerated category variables are converted to Mela value space"""
    result = copy(tree)
    result.stand_origin_relative_position = copy(tree.stand_origin_relative_position)
    return apply_mappers(result, *default_mela_tree_mappers)


def mela_stand(stand):
    """Convert a ForestStand so that enumerated category variables are converted to Mela value space"""
    result = copy(stand)
    result.geo_location = copy(stand.geo_location)
    result.stems_per_ha_scaling_factors = copy(stand.stems_per_ha_scaling_factors)
    result = apply_mappers(result, *default_mela_stand_mappers)
    result.reference_trees = list(map(mela_tree, result.reference_trees))
    for tree in result.reference_trees:
        tree.stand = result
    result.tree_strata = list(map(mela_stratum, result.tree_strata))
    for stratum in result.tree_strata:
        stratum.stand = result
    return result


default_mela_tree_mappers = [species_mapper]
default_mela_stratum_mappers = [species_mapper]
default_mela_stand_mappers = [stand_location_converter, stand_area_converter]
