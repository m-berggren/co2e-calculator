import unittest
import sys
sys.path.append("./co2e")

import pandas as pd
from ceva_co2e import CevaCO2e


def get_unlocode_data(csv_file: str) -> pd.DataFrame:
    return pd.read_csv(csv_file, delimiter=";")


class testCevaCO2e(unittest.TestCase):

    POL = "Hong Kong"
    POL_UNLOCODE = "HKHKG"

    POD = "Gothenburg"
    POD_UNLOCODE = "SEGOT"

    TRANSPORT = "LCL"
    WEIGHT = 201
    DF = get_unlocode_data("bin\ports-unlocode.csv")

    def test_get_unlocodes(self) -> tuple:
        result = CevaCO2e(self.POL, self.POD, self.TRANSPORT, self.WEIGHT, self.DF).get_unlocodes()
        self.assertEqual(result, (["HKHKG"], ["SEGOT"]))

    def test_response(self) -> bytes|None:
        result = CevaCO2e(self.POL, self.POD, self.TRANSPORT, self.WEIGHT, self.DF).response()
        self.assertEqual(result, 0.017)

if __name__ == '__main__':
    unittest.main()