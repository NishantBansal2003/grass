MODULE_TOPDIR = ../..

include $(MODULE_TOPDIR)/include/Make/Vars.make

PGM2 = r.mapcalc
PGM3 = r3.mapcalc
PROGRAMS = $(PGM2) $(PGM3)

r_mapcalc_OBJS  := $(filter-out map3.o xcoor3.o xres3.o, $(AUTO_OBJS))
r3_mapcalc_OBJS := $(filter-out map.o xcoor.o xres.o, $(AUTO_OBJS))

include $(MODULE_TOPDIR)/include/Make/Multi.make

EXTRA_CFLAGS = $(READLINEINCPATH) $(PTHREADINCPATH)
LIBES2 = $(CALCLIB) $(GISLIB) $(RASTERLIB) $(BTREELIB) $(READLINELIBPATH) $(READLINELIB) $(HISTORYLIB) $(PTHREADLIBPATH) $(PTHREADLIB) $(OPENMP_LIBPATH) $(OPENMP_LIB)
LIBES3 = $(CALCLIB) $(RASTER3DLIB) $(GISLIB) $(RASTERLIB) $(BTREELIB) $(READLINELIBPATH) $(READLINELIB) $(HISTORYLIB) $(PTHREADLIBPATH) $(PTHREADLIB) $(OPENMP_LIBPATH) $(OPENMP_LIB)
EXTRA_CFLAGS = $(OPENMP_CFLAGS)
EXTRA_INC = $(OPENMP_INCPATH)

default: multi

$(BIN)/$(PGM2)$(EXE): LIBES = $(LIBES2)
$(BIN)/$(PGM3)$(EXE): LIBES = $(LIBES3)

$(OBJDIR)/*.o $(OBJDIR)/mapcalc.yy.o: mapcalc.tab.h mapcalc.tab.c

.SECONDARY: mapcalc.tab.c mapcalc.tab.h mapcalc.output

.SECONDARY: mapcalc.yy.c
