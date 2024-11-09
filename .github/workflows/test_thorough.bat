set grass=%1
set python=%2


call %grass% --exec g.region s=0 n=90 w=0 e=100 b=0 t=1 rows=3 cols=3 res=10

call %grass% --exec r.mapcalc expr="a = int(row())"

call %grass% --exec r.colors map=a color=elevation

call %grass% --exec r.colors.out map="a" rules="-" format="json" color_format="hsv"



@REM call %grass% --tmp-project XY --exec %python% -m grass.gunittest.main --grassdata %USERPROFILE% --location nc_spm_full_v2alpha2 --location-type nc --min-success 96 --config .github\workflows\osgeo4w_gunittest.cfg
