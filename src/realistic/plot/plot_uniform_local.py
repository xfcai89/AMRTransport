import Ngl, Nio
import numpy as np


p0mb = 101325.
p0mb1 = 1013.25
interp = 1
extrap = False
pnew = [800., 750.]
lev = 0
f   = Nio.open_file("LowRes/LowRes_200610.01_tracer.nc")
# interpolation from sigma coordinate to pressure coordinate
# get parameters and variables for interpolation
hyam = f.variables["hyam"][:]/p0mb
hybm = f.variables["hybm"][:]
PS    = f.variables["aps"][:, :, :]

f   = Nio.open_file("Uniform/AMRDUST.nc")
DU_CI = f.variables["CI"][:, :, :, :]*1e6
DU_AI = f.variables["AI"][:, :, :, :]*1e6
lon_Uni   = f.variables["lon"][:]
lat_Uni   = f.variables["lat"][:]
lon_list = np.where((lon_Uni >= 330) & (lon_Uni <=360))[0].tolist()
lon_list += np.where((lon_Uni >= 0) & (lon_Uni <=90))[0].tolist()
lat_list = np.where((lat_Uni >= -10) & (lat_Uni <=50))[0].tolist()
lon_Uni  = np.where(lon_Uni > 180., lon_Uni - 360., lon_Uni)
# start the interpolation
NewTracer_CI_Uni = Ngl.vinth2p(DU_CI[:,:,:,:],hyam,hybm,pnew,PS[:,:,:],interp,p0mb1, 1,extrap)
NewTracer_AI_Uni = Ngl.vinth2p(DU_AI[:,:,:,:],hyam,hybm,pnew,PS[:,:,:],interp,p0mb1, 1,extrap)
NewTracer_AI_Uni = np.ma.masked_where(NewTracer_AI_Uni == 1.e30, NewTracer_AI_Uni)
print(np.max(NewTracer_AI_Uni))

# day 10 to 20
# set up colormap
rlist    = Ngl.Resources()
rlist.wkColorMap = "WhiteYellowOrangeRed"
for it in range(30):
    print(it)
    # use colormap and type information to setup output background
    wks_type = "pdf"
    wks = Ngl.open_wks(wks_type,"Uniform"+str(it), rlist)
    # resources for the contour
    res = Ngl.Resources()
    res.lbLabelBarOn          = False
    # Filled contour/labels/labelinfos
    res.cnLinesOn             = False
    res.cnFillOn              = True
    res.cnLineLabelsOn        = False
    res.cnInfoLabelOn         = False
    res.mpGridAndLimbOn       = False
    res.mpLimitMode       = "LatLon"              #-- must be set using minLatF/maxLatF/minLonF/maxLonF
    res.mpMinLatF         =  -10.                #-- sub-region minimum latitude
    res.mpMaxLatF         =  50.               #-- sub-region maximum latitude
    res.mpMinLonF         = -30.                 #-- sub-region minimum longitude
    res.mpMaxLonF         =  90.                  #-- sub-region maximum longitude       
    #anotherway to define colormap (overlay the predefined color map)
    # cmap = Ngl.read_colormap_file("WhiteBlueGreenYellowRed")
    #Level selection
    # res.lbBoxLinesOn  = False
    res.cnLevelSelectionMode   = "ExplicitLevels"   # Set explicit contour levels
    res.cnLevels               = np.arange(1e-5,8.e-4, 4e-5)      # 0,5,10,...,70
  
    # maximize the plot
    res.nglMaximize = True
    res.nglFrame = False
    # NewTracerPlot, LonPlot = Ngl.add_cyclic(NewTracer_AI_Uni[it, lev, :, :], lon_Uni)
    sliceTracer = NewTracer_AI_Uni[it, lev, lat_list, :]
    res.sfXArray = lon_Uni[lon_list]
    res.sfYArray = lat_Uni[lat_list]
    res.vpWidthF = 1
    res.vpHeightF = 0.5
    Ngl.contour_map(wks,sliceTracer[:, lon_list],res)

    Ngl.frame(wks)
    # Ngl.Draw(wks)
    Ngl.destroy(wks)
Ngl.end()
