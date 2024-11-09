set grass=%1
set python=%2



call %grass% --tmp-project XY --exec g.download.project url=https://grass.osgeo.org/sampledata/north_carolina/nc_spm_full_v2alpha2.tar.gz path=%USERPROFILE%

call %grass% --tmp-project XY --exec g.region s=0 n=90 w=0 e=100 b=0 t=1 rows=3 cols=3 res=10

call %grass% --tmp-project XY --exec r.mapcalc expr="a = int(row())"

call %grass% --tmp-project XY --exec r.colors map="a" color="elevation"

call %grass% --tmp-project XY --exec r.colors map="a" color="elevation"

call %grass% --tmp-project XY --exec r.colors.out map="a" rules="-" format="json" color_format="hsv"



@REM call %grass% --tmp-project XY --exec %python% -m grass.gunittest.main --grassdata %USERPROFILE% --location nc_spm_full_v2alpha2 --location-type nc --min-success 96 --config .github\workflows\osgeo4w_gunittest.cfg
