from forestdatamodel.model import ReferenceTree


class SupplementStrategy:
    def __init__(self, rt: ReferenceTree):
        self.reference_tree_id: str = rt.identifier
        self.solved: bool = False
        self.strategy: int = None
        self.tree_identifier: str = None
