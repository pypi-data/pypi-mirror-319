from pathlib import Path
import geopandas
def get_netherlands_shapefile():
    """
    Read in the shapefile from resrources/netherlands_shapefile, and convert to RD New.
    Assumes the code being run is in modules/plotting
    """
    shapefile= Path(Path(__file__).parent, "../resources/netherlands_shapefile/2019_provinciegrenzen_kustlijn.shp")
    if shapefile.exists():
        df = geopandas.read_file(shapefile, engine="pyogrio")
        shapefile_df = df.to_crs(28992)
        return shapefile_df
    else:
        return None