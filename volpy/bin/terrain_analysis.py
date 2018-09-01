class TerrainAnalysis():

    def __init__(self, survey, swell):
        self.survey = survey
        self.swell = swell

    def get_volumes(self, level):
        """"Returns the cut and fill volumes of a terrain, given a level"""
        # Returns a tuple
        pass

    def get_curves(self, step):
        """Returns all of the cut/fill volumes for different levels starting at
        the lowest and applying increasing step sizes iteratively.
        """
        # Return in a pandas dataframe
        pass