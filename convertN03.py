import geopandas as gpd
from pathlib import Path
# %%
filename = "N03-20240101"

if __name__ == "__main__":
    if not Path("./mlitdata/N03_GML/N03-20240101.shp").exists():
        print("N03-20240101.shp not found 国土数値情報からダウンロードしてください")
    gdf = gpd.read_file(f"./mlitdata/{filename}_GML/{filename}.shp")
    try:
        assert "N03_001" in gdf.columns
        assert gdf.N03_001.nunique() == 47
    except AssertionError as e:
        print(e)
        print("check failed")
        print(gdf.columns.tolist())
        print(gdf.N03_001.nunique())
        exit(1)
    print("check passed")
    export_dir_name = "parquet/N03"
    export_dir = Path(export_dir_name)
    export_dir.mkdir(parents=True, exist_ok=True)
    gdf.to_parquet(export_dir / f"{filename}.parquet")
    pref = gdf.N03_001.unique()
    for p in pref:
        _gdf = gdf[gdf.N03_001 == p]
        pref_code = _gdf.iloc[0].loc["N03_007"][:2]
        _gdf.to_parquet(export_dir / f"{filename}_{pref_code}.parquet")
