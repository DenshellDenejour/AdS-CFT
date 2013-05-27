from getBoundary import getBoundary
import numpy as np
import pylab as pl
from fig import fig, saveFig, printText, getPlotY
from printStatus import printRatio
from pickle import load, dump

hpsis=np.logspace(-6,1.5,300)
a2=0.0
plotImag=True
from solveBC import sweep, findrho

try:
    bbs,sols=load(open('cache/sols_a2='+str(a2)))
except IOError:
    print('Solve for sweep of different horizon BCs...')
    bbs,sols=sweep(lambda x,y: getBoundary(x,y,[0,a2]), hpsis, oscN=1, status=True)
    dump((bbs,sols),open('cache/sols_a2='+str(a2),'w'))

rho=-np.array(bbs)[:,:,1,1].real
rhoc=min([min(r) for r in rho])#rho, in units used at Tc

#Trs=[0.9,0.5,0.05]
nature=[10,17,28,40,54,71]
#murs=[i*17.5/nature[0] for i in nature]
murs=[i*19./nature[0] for i in nature]

zh=1
T=3./(zh*4.*np.pi)
#wvs= np.logspace(0,1.5,40)/15.

wvs= np.logspace(-3.2,2.075,40)
'''pl.xlim(wvs[0],wvs[-1])
if plotImag:
    pl.ylim(-1.1,1.8)
else:
    pl.ylim(-.1,1.8)'''

fig(0,size=10)
pl.xlim(0,wvs[-1])
pl.ylim(-0.4,1.3)
fig(1,size=10)
pl.ylim(-1.5,5)

pl.xlim(0,wvs[-1])

fig(0)
pl.plot([wvs[0],wvs[-1]],[1,1],c='r',ls='-',label='$\mu<1.75T$')
pl.legend(loc='lower right')
fig(1)
pl.plot([wvs[0],wvs[-1]],[0,0],c='r',ls='-',label='$\mu<1.75T$')
pl.legend(loc='upper right')


first=True
for j in range(len(murs)):
    #Tr=Trs[j]
    print('Solving for specific temperature...')
    #Tc=T*np.sqrt(rho/rhoc)

    rhoSol=findrho(lambda x,y: getBoundary(x,y,[0,a2]), sols, hpsis, bbs, murs[j]*T,ind=0)
    print('Solving for different frequencies...')
    sigmas=[]
    for osci in range(len(rhoSol)):
        bb,osc=getBoundary(rhoSol[osci][0],rhoSol[osci][1], [0,a2])
        def f(w):
            bb,osc=getBoundary(rhoSol[osci][0],rhoSol[osci][1], [w*T,a2])
            assert(osc==osci)
            return -1j*bb[2][1]/( bb[2][0]*(T*w) )
        nwvs,_,nsigmas=getPlotY(wvs[0],wvs[-1],f,lambda s:s.real,minN=100,maxTurn=0.1)
        sigmas.append((nwvs,nsigmas))
    for s in sigmas:
        fig(0)
        pl.plot(s[0],[i.real for i in s[1]],ls='-',c='k')
        printText(s[0],[i.real for i in s[1]],0.6,0,'$'+str(nature[j])+'\mu_0$')
        if plotImag:
            fig(1)
            pl.plot(s[0],[i.imag for i in s[1]],ls='-',c='k')
            printText(s[0],[i.imag for i in s[1]],1.,0,'$'+str(nature[j])+'\mu_0$')
        first=False

print('$\mu_0=%.1fT$'%(murs[0]/nature[0]))
#pl.plot([wvs[0],wvs[-1]],[1,1],ls=':',c='k')
#pl.plot([wvs[0],wvs[-1]],[0,0],ls=':',c='k')
#printText([wvs[0],wvs[-1]],[1,1],0,5.,r'$\sigma=1$')
#pl.legend(loc=3)
#pl.legend(loc='upper right')
fig(0)
pl.xlabel(r'$\frac{\omega}{T}$')
pl.xlabel(r'$\mathrm{Re}(\sigma)$')
saveFig('graphene2_cond_re_a2_'+str(a2))
fig(1)
pl.xlabel(r'$\frac{\omega}{T}$')
pl.xlabel(r'$\mathrm{Im}(\sigma)$')
saveFig('graphene2_cond_im_a2_'+str(a2))
pl.show()
