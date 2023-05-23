class P:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class ThaumInteractor:
    pointWritingMaterials: P
    pointScrolls: P
    rectAspectsListingLT: P
    rectAspectsListingRB: P
    pointAspectsScrollLeft: P
    pointAspectsScrollRight: P
    pointAspectsMixLeft: P
    pointAspectsMixCreate: P
    pointAspectsMixRight: P
    rectInventoryLT: P
    rectInventoryRB: P
    rectHexagonsLT: P
    rectHexagonsRB: P

    def __init__(self, controlsConfig):
        conf = controlsConfig
        self.pointWritingMaterials = P(conf['pointWritingMaterials']['x'], conf['pointWritingMaterials']['y'])
        self.pointScrolls = P(conf['pointScrolls']['x'], conf['pointScrolls']['y'])
        self.rectAspectsListingLT = P(conf['rectAspectsListingLT']['x'], conf['rectAspectsListingLT']['y'])
        self.rectAspectsListingRB = P(conf['rectAspectsListingRB']['x'], conf['rectAspectsListingRB']['y'])
        self.pointAspectsScrollLeft = P(conf['pointAspectsScrollLeft']['x'], conf['pointAspectsScrollLeft']['y'])
        self.pointAspectsScrollRight = P(conf['pointAspectsScrollRight']['x'], conf['pointAspectsScrollRight']['y'])
        self.pointAspectsMixLeft = P(conf['pointAspectsMixLeft']['x'], conf['pointAspectsMixLeft']['y'])
        self.pointAspectsMixCreate = P(conf['pointAspectsMixCreate']['x'], conf['pointAspectsMixCreate']['y'])
        self.pointAspectsMixRight = P(conf['pointAspectsMixRight']['x'], conf['pointAspectsMixRight']['y'])
        self.rectInventoryLT = P(conf['rectInventoryLT']['x'], conf['rectInventoryLT']['y'])
        self.rectInventoryRB = P(conf['rectInventoryRB']['x'], conf['rectInventoryRB']['y'])
        self.rectHexagonsLT = P(conf['rectHexagonsLT']['x'], conf['rectHexagonsLT']['y'])
        self.rectHexagonsRB = P(conf['rectHexagonsRB']['x'], conf['rectHexagonsRB']['y'])
