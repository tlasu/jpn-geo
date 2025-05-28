import io
from pathlib import Path

import geopandas as gpd
import requests

def get_pref_gdf(gyosei_code:str):
    """
    行政コードを指定して、指定した行政地域のgeodataframeを取得する
    gyosei_code: 行政コード
    """
    assert len(gyosei_code) == 5
    #08220
    pref_code = gyosei_code[:2]
    url = f"https://raw.githubusercontent.com/tlasu/jpn-geo/master/parquet/N03/N03-20240101_{pref_code}.parquet"
    response = requests.get(url).content
    gdf = gpd.read_parquet(io.BytesIO(response))
    return gdf[gdf.N03_007 == gyosei_code]

if __name__ == "__main__":
    gyosei_code = "08220"
    gdf = get_pref_gdf("08220").to_parquet(f"{gyosei_code}.parquet")
# %%
