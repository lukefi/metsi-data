from forestdatamodel.enums.vmi import VmiLandUseCategory, VmiSpecies
from forestdatamodel.enums.internal import LandUseCategory, TreeSpecies

species_map = {
    VmiSpecies.PINE: TreeSpecies.PINE,
    VmiSpecies.SPRUCE: TreeSpecies.SPRUCE,
    VmiSpecies.SILVER_BIRCH: TreeSpecies.SILVER_BIRCH,
    VmiSpecies.DOWNY_BIRCH: TreeSpecies.DOWNY_BIRCH,
    VmiSpecies.ASPEN: TreeSpecies.ASPEN,
    VmiSpecies.GREY_ALDER: TreeSpecies.GREY_ALDER,
    VmiSpecies.COMMON_ALDER: TreeSpecies.COMMON_ALDER,
    VmiSpecies.MOUNTAIN_ASH: TreeSpecies.MOUNTAIN_ASH,
    VmiSpecies.GOAT_WILLOW: TreeSpecies.GOAT_WILLOW,
    VmiSpecies.OTHER_CONIFEROUS: TreeSpecies.OTHER_CONIFEROUS,
    VmiSpecies.SHORE_PINE: TreeSpecies.SHORE_PINE,
    VmiSpecies.KEDAR: TreeSpecies.KEDAR,
    VmiSpecies.OTHER_PINE: TreeSpecies.OTHER_PINE,
    VmiSpecies.LARCH: TreeSpecies.LARCH,
    VmiSpecies.ABIES: TreeSpecies.ABIES,
    VmiSpecies.OTHER_SPRUCE: TreeSpecies.OTHER_SPRUCE,
    VmiSpecies.THUJA: TreeSpecies.THUJA,
    VmiSpecies.JUNIPER: TreeSpecies.JUNIPER,
    VmiSpecies.YEW: TreeSpecies.YEW,
    VmiSpecies.OTHER_DECIDUOUS: TreeSpecies.OTHER_DECIDUOUS,
    VmiSpecies.BAY_WILLOW: TreeSpecies.BAY_WILLOW,
    VmiSpecies.EUROPEAN_WHITE_ELM: TreeSpecies.EUROPEAN_WHITE_ELM,
    VmiSpecies.WYCH_ELM: TreeSpecies.WYCH_ELM,
    VmiSpecies.SMALL_LEAVED_LIME: TreeSpecies.SMALL_LEAVED_LIME,
    VmiSpecies.POPLAR: TreeSpecies.POPLAR,
    VmiSpecies.COMMON_ASH: TreeSpecies.COMMON_ASH,
    VmiSpecies.OAK: TreeSpecies.OAK,
    VmiSpecies.BIRD_CHERRY: TreeSpecies.BIRD_CHERRY,
    VmiSpecies.MAPLE: TreeSpecies.MAPLE,
    VmiSpecies.HAZEL: TreeSpecies.HAZEL,
    VmiSpecies.UNKNOWN: TreeSpecies.UNKNOWN,
}

land_use_map = {
    VmiLandUseCategory.FOREST: LandUseCategory.FOREST,
    VmiLandUseCategory.SCRUB_LAND: LandUseCategory.SCRUB_LAND,
    VmiLandUseCategory.WASTE_LAND: LandUseCategory.WASTE_LAND,
    VmiLandUseCategory.OTHER_FOREST: LandUseCategory.OTHER_FOREST,
    VmiLandUseCategory.AGRICULTURAL: LandUseCategory.AGRICULTURAL,
    VmiLandUseCategory.BUILT_LAND: LandUseCategory.BUILT_LAND,
    VmiLandUseCategory.ROAD: LandUseCategory.ROAD,
    VmiLandUseCategory.ENERGY_TRANSMISSION_LINE: LandUseCategory.ENERGY_TRANSMISSION_LINE,
    VmiLandUseCategory.FRESHWATER: LandUseCategory.FRESHWATER,
    VmiLandUseCategory.SEA: LandUseCategory.SEA
}

def convert_land_use_category(lu_code: str) -> LandUseCategory:
    value = lu_code.upper() #in case it is "a" instead of "A"
    vmi_category = VmiLandUseCategory(value)
    return land_use_map.get(vmi_category)

def convert_species(species_code: str) -> TreeSpecies:
    """Converts VMI species code to internal TreeSpecies code"""
    value = species_code.strip()
    vmi_species = VmiSpecies(value)
    return species_map.get(vmi_species)