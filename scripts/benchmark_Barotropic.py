############################
# Preamble
############################
from common import *

sd0 = 5
np.random.seed(sd0)

############################
# Setup
############################
from mods.Barotropic.defaults  import setup
#

setup.t.T = 20

BAMs = BAM_list()
BAMs.add(Climatology)
BAMs.add(EnKF,infl=1.15,keep=True,upd_a='Sqrt')
BAMs.add(LETKF  ,infl=1.10,locf=setup.locf(100,'x2y'),keep=True)
#BAMs.add(LETKF,infl=1.10,locf=setup.locf(10,'x2y'),upd_a='approx',keep=True)
#BAMs.add(SL_EAKF,infl=1.0,locf=setup.locf(10,'y2x'),keep=True)

############################
# Common settings
############################
for method in BAMs:
  method.N       = 20
  method.rot     = False

############################
# Assimilate
############################
ss   = np.empty(len(BAMs),dict)
kept = []

xx,yy = simulate(setup)
for k,method in enumerate(BAMs):
  seed(sd0)
  stats = assimilate(setup,method,xx,yy)
  ss[k] = stats.average_in_time()
  if getattr(method,'keep',False): kept.append(stats)
print_averages(BAMs,ss)


############################
# Plot
############################
k=0
for method in BAMs:
  if getattr(method,'keep',False):
    stats = kept[k]
    k += 1
    plot_time_series(xx,stats,setup.t,dim=2)
    plot_ens_stats(xx,stats,setup.t,method)
    plot_3D_trajectory(xx[:,:3],stats,setup.t)


