import numpy, pylab
from scipy import interpolate
import sys

A = numpy.loadtxt('data/ZERO_DET_high_P.txt')


fmin = 9.
fmax = 1570. #FIXME allow different masses?

#
# Constants
#

LAL_MTSUN_SI = 4.9254909500000001e-06
PI = 3.14159265

#
# Mchirp
#

def mchirp(m1, m2):
        return (m1 * m2)**.6 / (m1+m2)**.2

#
# cumulative fractional snr computed over f
#

def snr(f, asd):
	df = f[1] - f[0]
	out = numpy.cumsum(df * f**(-7./3) / asd(f)**2)**.5
	return out# / out[-1]

#
# frequency to time relationship assuming 0PN 
#

def freq_to_time(Mc,f):
	Mc = Mc * LAL_MTSUN_SI
	return 5. * Mc / 256. * (PI * Mc * f) ** (-8./3.)

# define a frequency array
f = numpy.linspace(fmin, fmax, 10000)

# work out the time to coalescence at a given f
t = freq_to_time(mchirp(1.4,1.4),f) # FIXME dont hardcode masses

# interpolate the asd
asd = interpolate.interp1d(A[:,0], A[:,1])

# compute the snr on the frequency array
snrd = snr(f, asd)

h = (8**2 / snrd[-1]) * f ** (-7./6)
hplus = h * (40./400.) ** (2./3)
hminus = h * (40./4.) ** (2./3)
pylab.figure(figsize=(6, 5))
pylab.loglog(A[:, 0], A[:, 1], color='k', lw=2)
pylab.loglog(f, h, color='#800000', lw=2)
pylab.loglog(f, hplus, color='#800000', lw=0.5)
pylab.loglog(f, hminus, color='#800000', lw=0.5)
pylab.fill_between(f, hplus, hminus, color='#FFD9BF')
for tt in (1, 10, 100):
	pylab.axvline(max(f[t >= tt]), linestyle='--', color='k')
	pylab.text(1.1 * max(f[t >= tt]), 4e-22, '%d s\nbefore\nmerger' % tt)
pylab.xlim(9, 1570)
pylab.ylim(1e-24, 1e-21)
pylab.xlabel(r'frequency (s)')
pylab.ylabel(r'amplitude spectral density (Hz$^{\frac{1}{2}}$)')
#pylab.grid()
pylab.gca().set_axis_bgcolor('#E6E6E6')
pylab.subplots_adjust(bottom=0.15,top=0.95,left=0.15,right=0.95)
pylab.savefig(sys.argv[1])
