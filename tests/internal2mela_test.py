import unittest
from parameterized import parameterized
from forestdatamodel.model import ReferenceTree, ForestStand, TreeStratum
from forestdatamodel.conversion.internal2mela import species_mapper, mela_stand
from forestdatamodel.enums.internal import LandUseCategory, OwnerCategory, TreeSpecies
from forestdatamodel.enums.mela import MelaLandUseCategory, MelaOwnerCategory, MelaTreeSpecies


class Internal2MelaTest(unittest.TestCase):
    def test_species_good(self):
        fixture = ReferenceTree()
        fixture.species = TreeSpecies.THUJA
        result = species_mapper(fixture)
        self.assertEqual(MelaTreeSpecies.OTHER_CONIFEROUS, result.species)

    def test_species_unknown(self):
        fixture = ReferenceTree()
        fixture.species = None
        result = species_mapper(fixture)
        self.assertEqual(MelaTreeSpecies.OTHER_DECIDUOUS, result.species)

    def test_stand_species_conversion(self):
        fixture = ForestStand(geo_location=(6654200, 102598, 0.0, "EPSG:3067"), area=100.0, area_weight=100.0, auxiliary_stand=True)
        tree = ReferenceTree(species=TreeSpecies.SPRUCE, stand=fixture)
        stratum = TreeStratum(species=TreeSpecies.PINE, stand=fixture)
        fixture.reference_trees.append(tree)
        fixture.tree_strata.append(stratum)
        result = mela_stand(fixture)
        self.assertEqual(MelaTreeSpecies.NORWAY_SPRUCE, result.reference_trees[0].species)
        self.assertEqual(MelaTreeSpecies.SCOTS_PINE, result.tree_strata[0].species)
        self.assertEqual((6654.2, 102.598, 0.0, "EPSG:3067"), result.geo_location)
        self.assertEqual(0.0, result.area)
        self.assertEqual(100.0, result.area_weight)

    def test_owner_category(self):
        fixture = ForestStand()
        fixture.owner_category = OwnerCategory.METSAHALLITUS
        result = mela_stand(fixture)
        self.assertEqual(MelaOwnerCategory.STATE, result.owner_category)

        #ownerCategory UNKNOWN should convert to MelaOwnerCategory PRIVATE
        fixture2 = ForestStand()
        fixture2.owner_category = OwnerCategory.UNKNOWN
        result = mela_stand(fixture2)
        self.assertEqual(MelaOwnerCategory.PRIVATE, result.owner_category)

    @parameterized.expand([
        (LandUseCategory.FOREST, MelaLandUseCategory.FOREST_LAND),
        (LandUseCategory.ROAD, MelaLandUseCategory.ROADS_OR_ELECTRIC_LINES),
        (LandUseCategory.REAL_ESTATE, MelaLandUseCategory.BUILT_UP_LAND),
        (LandUseCategory.OTHER_LAND, MelaLandUseCategory.ROADS_OR_ELECTRIC_LINES),
        (LandUseCategory.WATER_BODY, MelaLandUseCategory.LAKES_AND_RIVERS),
    ])
    def test_land_use_category(self, lu_category, expected):
        fixture = ForestStand(land_use_category=lu_category)
        result = mela_stand(fixture)
        self.assertEqual(result.land_use_category, expected)
