from forestdatamodel.enums.forest_centre import ForestCentreLandUseCategory, ForestCentreSpecies, ForestCentreLandUseCategory
from forestdatamodel.enums.internal import TreeSpecies, LandUseCategory

species_map = {
    ForestCentreSpecies.PINE: TreeSpecies.PINE,
    ForestCentreSpecies.SPRUCE: TreeSpecies.SPRUCE,
    ForestCentreSpecies.SILVER_BIRCH: TreeSpecies.SILVER_BIRCH,
    ForestCentreSpecies.DOWNY_BIRCH: TreeSpecies.DOWNY_BIRCH,
    ForestCentreSpecies.ASPEN: TreeSpecies.ASPEN,
    ForestCentreSpecies.GREY_ALDER: TreeSpecies.GREY_ALDER,
    ForestCentreSpecies.COMMON_ALDER: TreeSpecies.COMMON_ALDER,
    ForestCentreSpecies.OTHER_CONIFEROUS: TreeSpecies.OTHER_CONIFEROUS,
    ForestCentreSpecies.OTHER_DECIDUOUS: TreeSpecies.OTHER_DECIDUOUS,
    ForestCentreSpecies.DOUGLAS_FIR: TreeSpecies.DOUGLAS_FIR,
    ForestCentreSpecies.JUNIPER: TreeSpecies.JUNIPER,
    ForestCentreSpecies.SHORE_PINE: TreeSpecies.SHORE_PINE,
    ForestCentreSpecies.EUROPEAN_WHITE_ELM: TreeSpecies.EUROPEAN_WHITE_ELM,
    ForestCentreSpecies.LARCH: TreeSpecies.LARCH,
    ForestCentreSpecies.SMALL_LEAVED_LIME: TreeSpecies.SMALL_LEAVED_LIME,
    ForestCentreSpecies.BLACK_SPRUCE: TreeSpecies.BLACK_SPRUCE,
    ForestCentreSpecies.WILLOW: TreeSpecies.WILLOW,
    ForestCentreSpecies.MOUNTAIN_ASH: TreeSpecies.MOUNTAIN_ASH,
    ForestCentreSpecies.ABIES: TreeSpecies.ABIES,
    ForestCentreSpecies.GOAT_WILLOW: TreeSpecies.GOAT_WILLOW,
    ForestCentreSpecies.COMMON_ASH: TreeSpecies.COMMON_ASH,
    ForestCentreSpecies.KEDAR: TreeSpecies.KEDAR,
    ForestCentreSpecies.SERBIAN_SPRUCE: TreeSpecies.SERBIAN_SPRUCE,
    ForestCentreSpecies.OAK: TreeSpecies.OAK,
    ForestCentreSpecies.BIRD_CHERRY: TreeSpecies.BIRD_CHERRY,
    ForestCentreSpecies.MAPLE: TreeSpecies.MAPLE,
    ForestCentreSpecies.CURLY_BIRCH: TreeSpecies.CURLY_BIRCH,
    ForestCentreSpecies.WYCH_ELM: TreeSpecies.WYCH_ELM,
    ForestCentreSpecies.UNKNOWN_CONIFEROUS: TreeSpecies.UNKNOWN_CONIFEROUS,
    ForestCentreSpecies.UNKNOWN_DECIDUOUS: TreeSpecies.UNKNOWN_DECIDUOUS,
}

land_use_map = {
    ForestCentreLandUseCategory.FOREST: LandUseCategory.FOREST,
    ForestCentreLandUseCategory.SCRUB_LAND: LandUseCategory.SCRUB_LAND,
    ForestCentreLandUseCategory.WASTE_LAND: LandUseCategory.WASTE_LAND,
    ForestCentreLandUseCategory.OTHER_FOREST: LandUseCategory.OTHER_FOREST,
    ForestCentreLandUseCategory.AGRICULTURAL: LandUseCategory.AGRICULTURAL,
    ForestCentreLandUseCategory.REAL_ESTATE: LandUseCategory.REAL_ESTATE,
    ForestCentreLandUseCategory.OTHER_LAND: LandUseCategory.OTHER_LAND,
    ForestCentreLandUseCategory.WATER_BODY: LandUseCategory.WATER_BODY
}

def convert_land_use_category(lu_code: str) -> LandUseCategory:
    fc_category = ForestCentreLandUseCategory(lu_code)
    return land_use_map.get(fc_category)

def convert_species(species_code: str) -> TreeSpecies:
    """Converts FC species code to internal TreeSpecies code"""
    fc_species = ForestCentreSpecies(species_code)
    return species_map.get(fc_species)