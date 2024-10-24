import numpy as np
import json
import pandas as pd
import py_windblade_opa.airfoils.af_naca4415_test as afs
import logging

class BladeGeometry:
    _bg_version:str = "1.0"
    R:float = None
    bl_Ri:np.ndarray = None
    bl_c_i:np.ndarray = None
    _no_sections:int = None
    pitch:np.ndarray = None  # pitch angle

    # the following probably should be moved to another class (e.g. BladeCalc)
    lambda0:float = None # lambda at tip of blade
    # bl_a_i:np.ndarray = None  # attack angle
    # m_lambdaE_i:np.ndarray = None  # flow angle (inverse) parameter
    

    def __init__(self, R:float, r_is:np.ndarray,
                 lambda0:float, 
                 chords:np.ndarray,
                 pitch:np.ndarray, airfoil:list=None, no_sections:int = None):
        self.R = R
        self.bl_c_i = chords
        self.bl_Ri = r_is
        self._no_sections = len(chords)
        
        # assert for pitch
        if pitch is None:
            pitch = np.zeros(self._no_sections)
        elif isinstance(pitch, (int, float)):
            pitch = np.ones(self._no_sections) * pitch
        elif isinstance(pitch, np.ndarray):
            if len(pitch) != self._no_sections:
                raise ValueError("The pitch array must have the same length as the chord array")
            pitch = pitch
        else:
            raise ValueError("The pitch must be a float, int or numpy array")
        self.pitch = pitch 
        self.lambda0 = lambda0
        # remove the following 
        # TODO this is temporary until the airfoils are properly implemented
        self.airfoils_lst = airfoil if airfoil is not None else [afs.NACAtest(0.15) for i in range(self._no_sections)]

    @property  
    def no_sections(self):
        """Number of sections in the blade	
        """
        return self._no_sections
    

    def to_dict(self):
        """Convert blade geometry data to a dictionary

        Returns:
            _type_: _description_
        """
        dic = {
            "blade_geom_version": self._bg_version,
            "R": self.R,
            "r_is": self.bl_Ri.tolist(),
            "chords": self.bl_c_i.tolist(),
            "pitch": self.pitch.tolist(),
            "lambda0": self.lambda0,
            "no_sections": self.no_sections   
        }
        return dic
    
    def to_df(self):
        """Convert blade geometry data to a pandas DataFrame

        Returns:
            pd.DataFrame: blade geometry data
        """
                
        return pd.DataFrame({
            "r_is": self.bl_Ri.tolist(),
            "chords": self.bl_c_i.tolist(),
            "pitch": self.pitch.tolist()}
            )
        
    # save to disk
    def to_json(self, file:str):
        """Save blade geometry data to disk

        Args:
            file (str): _description_
        """
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @classmethod
    def from_json(cls, file:str):
        """Load blade geometry data from disk

        Args:
            file (str): _description_

        Returns:
            BladeGeometry: blade geometry object
        """
        # raise NotImplementedError("This method is not properly implemented yet")
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bgversion = data.pop("blade_geom_version", None)
        logging.info("Loading blade geometry version %s",bgversion)
        R = data.get("R")
        r_is = np.array(data.get("r_is"))
        chords = np.array(data.get("chords"))
        pitch = np.array(data.get("pitch"))
        lambda0 = data.get("lambda0")
        no_sections = data.get("no_sections")
        airfoils = data.get("airfoils", None)
        assert no_sections == len(r_is) == len(chords) == len(pitch), "The number of sections must be the same for all arrays"
        return cls(R=R, r_is=r_is, lambda0=lambda0, chords=chords, pitch=pitch, airfoil=airfoils)

# I want to write tests for the to_dict, to_df and to_json methods, and from_json method



