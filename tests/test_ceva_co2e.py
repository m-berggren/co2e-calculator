import unittest

import pandas as pd

from co2e.ceva_co2e import CevaCO2e


def get_unlocode_data(csv_file: str) -> pd.DataFrame:
    return pd.read_csv(csv_file, delimiter=";")


class testCevaCO2e(unittest.TestCase):

    POL = "Cape Town"
    POD = "Dar es Salaam"
    TRANSPORT = "FCL"
    WEIGHT = 7039
    DF = get_unlocode_data("bin\ports-unlocode.csv")

    def test_get_unlocodes(self) -> tuple:
        result = CevaCO2e(self.POL, self.POD, self.TRANSPORT, self.WEIGHT, self.DF).get_unlocodes()
        self.assertEqual(result, (["ZACPT"], ["TZDAR"]))

    def test_response(self) -> bytes|None:
        result = CevaCO2e(self.POL, self.POD, self.TRANSPORT, self.WEIGHT, self.DF).response()
        self.assertEqual(result, 0.424)