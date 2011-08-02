import pylab
import sys

pylab.figure(figsize=(5, 4))
a = pylab.linspace(0., 1., 1000.)
pylab.plot(a, 2 * (1 + a) / a, 'k', lw=2)
pylab.ylim(0, 40)
pylab.xlabel('(latency) / (template length)')
pylab.ylabel(r'operations / sample / $\lg (\textrm{template length})$')
pylab.gca().set_axis_bgcolor('#E6E6E6')
pylab.savefig(sys.argv[1])