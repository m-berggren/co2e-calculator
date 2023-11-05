import json

import pandas as pd
import requests


class CevaCO2e:
    def __init__(self, pol: str, pod: str, transport: str, weight: float, df: pd.DataFrame) -> None:
        self.transport = transport.strip()
        self.pol = pol.strip()
        self.pod = pod.strip()
        self.weight = weight
        self.df = df
        

    def get_unlocodes(self):
        df = self.df

        """ Check if Port of loading (UNLOCODE) exists in Dataframe['UNLOCODE'].
        If not then search for Port name in Dataframe['NAME'] and get UNLOCODE.
        """
        
        if self.pol.lower() in set(df.UNLOCODE.str.lower()):
            pol = [self.pol] #  Enclosed in [] to mimic falsy value
        else:
            pol = df.loc[df.NAME == self.pol, 'UNLOCODE'].values

        if self.pod in set(df.UNLOCODE.str.lower()):
            pod = [self.pod] #  Enclosed in [] to mimic falsy value
        else:
            pod = df.loc[df.NAME == self.pod, 'UNLOCODE'].values

        return pol, pod


    def parse_info(self) -> str:

        """ Will parse website differently depending on if Air shipment or Sea.
        """

        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "user-agent": "Mozilla/5.0",
        }

        if self.transport == "AIR":
            # IATA airport codes are 3 letters long
            if len(self.pol) == 3 and len(self.pod) == 3:
                weight = self.weight
                url = f"https://my.cevalogistics.com/api/wso2/proxy/searoutes/co2emissions/1.0.0/air?fromIata={self.pol}&toIata={self.pod}&weight={weight}"

            else:
                return None

        else:
            pol, pod = self.get_unlocodes()

            if pol and pod:
                # Divide by 1000 for tonne and 10 for 1 TEU eq.
                weight = self.weight / 10_000
                
                url = f"https://my.cevalogistics.com/api/wso2/proxy/searoutes/co2emissions/1.0.0/sea?fromLocode={pol[0]}&toLocode={pod[0]}&nContainers={weight}&containerSize=20"
                
            else:
                return None

        response = requests.get(url, headers=headers)

        return response.content


    def response(self) -> float:
        string = self.parse_info()

        if not string:
            return None

        json_dict = json.loads(string.decode("utf-8"))["co2e"]

        return round(json_dict["ttw"] / 1_000_000, 3)
