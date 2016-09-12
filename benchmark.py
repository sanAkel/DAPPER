############################
# Preamble
############################
from common import *

np.random.seed(5)
#LCG(5)


############################
# Setup
############################

#from mods.Lorenz63.sak12 import setup
# Expected rmse_a = 0.63 (sak 0.65)
#cfg           = DAM(EnKF)
#cfg.N         = 10
#cfg.infl      = 1.02
#cfg.AMethod   = 'Sqrt'
#cfg.rot       = True
#
#cfg.da_method = iEnKF # rmse_a = 0.31
#cfg.iMax      = 10
#
#cfg           = DAM(PartFilt) # rmse_a = 0.275 (N=4000)
#cfg.N         = 800
#cfg.NER       = 0.1
#
#setup.t.dkObs = 10
#cfg = DAM(ExtKF, infl = 1.05)


from mods.MAOOAM.maooam16 import setup
#
cfg           = DAM(EnKF_N)
cfg.N         = 15
cfg.rot       = False
#
#cfg = DAM(Climatology)
#cfg = DAM(D3Var)
#cfg = DAM(ExtKF, infl = 1.05)
#cfg = DAM(EnsCheat)

#from mods.Lorenz95.spectral_obs import setup
#from mods.Lorenz95.m33 import setup

#from mods.LA.raanes2014 import setup


############################
# Common
############################
# setup.t.T = 1600
cfg.liveplotting = False 


############################
# Generate synthetic truth/obs
############################
# xx=np.loadtxt('./data/truthref.dat')

# f,hatm,h,chrono,X0 = setup.f, setup.hatm, setup.h, setup.t, setup.X0
# # obs
# yyatm = zeros((chrono.KObs+1,hatm.m))
# for k,t in enumerate(chrono.ttObs):
#   yyatm[k] = hatm.model(xx[chrono.kkObs[k]],t) + hatm.noise.sample(1)

# yy = zeros((chrono.KObs+1,h.m))
# for k,t in enumerate(chrono.ttObs):
#   yy[k] = h.model(xx[chrono.kkObs[k]],t) + h.noise.sample(1)
xx,yy = simulate(setup)
yyatm=yy
############################
# Assimilate
############################
s = assimilate(setup,cfg,xx,yyatm,yy)


############################
# Report averages
############################
chrono = setup.t
kk_a = chrono.kkObsBI
kk_f = chrono.kkObsBI-1
print('Mean analysis RMSE: {: 8.5f} ± {:<5g},    RMV: {:8.5f}'
    .format(*series_mean_with_conf(s.rmse[kk_a]),mean(s.rmv[kk_a])))
print('Mean forecast RMSE: {: 8.5f} ± {:<5g},    RMV: {:8.5f}'
    .format(*series_mean_with_conf(s.rmse[kk_f]),mean(s.rmv[kk_f])))
print('Mean analysis MGSL: {: 8.5f} ± {:<5g}'
    .format(*series_mean_with_conf(s.logp_m[kk_a])))

############################
# Plot
############################
# plot_time_series(xx,s,chrono,dim=2)
# plot_ens_stats(xx,s,chrono,cfg)
# plot_3D_trajectory(xx[:,:3],s,chrono)
