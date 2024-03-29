#!/usr/bin/env python

from optparse import OptionParser, Option
from pylal import spawaveform
import numpy as np
import matplotlib
from operator import attrgetter
import pylab
from itertools import groupby, izip
import sys

def take_last(it):
    while True:
        try:
            val = it.next()
        except StopIteration:
            return val

# setting some figure properties
# taken from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
fig_width_pt = 525  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width * golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
matplotlib.rcParams.update(
  {'axes.labelsize': 24,
   'axes.linewidth': 2,
   'grid.linewidth': 1.5,
   'font.size': 16,
   'legend.fontsize': 20,
   'lines.linewidth': 2,
   'xtick.labelsize': 24,
   'ytick.labelsize': 24,
   'figure.figsize': fig_size,
   })

# Place time slices

# Generate plot
from gstlal.svd_bank import read_banks
bank, = read_banks('data/svd_0_9999.xml')
pylab.figure(figsize=fig_size)
ax = pylab.subplot(111, xscale="log")
legend_artists = []
legend_labels = []
num_rates = len(set(x.rate for x in bank.bank_fragments))
tmax = max(x.end for x in bank.bank_fragments)
mc = spawaveform.chirpmass(1.4, 1.4)
for color, (rate, fragments) in izip(('black', '#E6E6E6', 'white', '#FFD9BF', '#BFBFDF', '#FFBFBF'), groupby(bank.bank_fragments, attrgetter('rate'))):
	legend_artists += [pylab.Rectangle((0, 0), 1, 1, facecolor = color)]
	legend_labels += ['%d Hz' % rate]
	for fragment in fragments:
		t = pylab.linspace(max(fragment.start, 1./4096), fragment.end)
		a = (0.2 * t / mc) ** (-1./4)
		# FIXME: PGF backend doesn't like filled shapes that extend beyond axes.
		# See https://github.com/matplotlib/matplotlib/issues/2885.
		pylab.fill_between(t[t >= 2e-1], -a[t >= 2e-1], a[t >= 2e-1], facecolor = color)
pylab.legend(reversed(legend_artists), reversed(legend_labels), loc='lower left', ncol=3)
pylab.xlim(tmax, 2e-1)
pylab.ylim(-.1, .1)
pylab.yticks([], [])
pylab.xticks([take_last(x).end for _, x in groupby(bank.bank_fragments, attrgetter("rate"))], ["$%.1f$" % take_last(x).end for _, x in groupby(bank.bank_fragments, attrgetter("rate"))], rotation=45)
for x in reversed(bank.bank_fragments):
	t = pylab.text((x.end * max(x.start, pylab.xlim()[1]))**0.5, 0, str(len(x.orthogonal_template_bank)), horizontalalignment="center",
		verticalalignment="center", rotation=90)
t.set_color("w")  # XXX: hard-code white text for the last text entry
pylab.grid()
pylab.xlabel('time before coalescence (s)')
pylab.ylabel(r'strain amplitude')
pylab.subplots_adjust(left=0.06, right=0.97, top=0.99, bottom=0.3)
pylab.gca().set_axis_bgcolor('#E6E6E6')
pylab.savefig(sys.argv[1])
