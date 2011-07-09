#!/usr/bin/env python

from gstlal import lloidplots
from glue.ligolw import utils, lsctables
import pylab
from matplotlib import ticker
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import sys

column1 = 'mchirp'
column2 = 'mtotal'

small_table = lsctables.table.get_table(
	utils.load_filename('data/tmpltbank.xml'),
	lsctables.SnglInspiralTable.tableName
)
n_small_templates = len(small_table)
small_data = zip(small_table.get_column(column1), small_table.get_column(column2))

# Create fill area (paint low chirp mass area black and skip drawing points there
# in order to create a smaller PDF file

@pylab.vectorize
def soln(mchirp):
	return pylab.roots([1., 0., -mchirp**(5./3), -1])[0]**3	

fill_mtotal = pylab.linspace(2., 6., 50)
fill_min_mchirp = 2 ** (-6./5) * fill_mtotal
fill_max_mchirp = (fill_mtotal - 1) ** (3./5) * fill_mtotal ** (-1./5)
#min_mchirp = 2. ** (-6./5) * 2.
#max_big_mchirp = 5. ** (3./5) / 6. ** (1./5)
#fill_mchirp = pylab.linspace(min_mchirp, max_big_mchirp, 50)
#fill_min_mtotal = 2 ** (6./5) * fill_mchirp
#fill_max_mtotal = soln(fill_mchirp)

big_table = lsctables.table.get_table(
	utils.load_filename('data/tmpltbank-pruned.xml'),
	lsctables.SnglInspiralTable.tableName
)
n_big_templates = len(big_table)
big_data = [x for x in zip(big_table.get_column(column1), big_table.get_column(column2)) if x not in small_data]
#big_data2 = [x for x in big_data if x[0] >= max_big_mchirp]

small_data = zip(*small_data)
big_data = zip(*big_data)

def foo():
	pylab.fill_betweenx(fill_mtotal, fill_min_mchirp, fill_max_mchirp, edgecolor='#800000', facecolor='#FFBFBF')
	#pylab.plot(big_data[0], big_data[1], ',k', markersize=0.01)
	pylab.plot(small_data[0], small_data[1], ',k')
	#pylab.fill_between(fill_mchirp, fill_min_mtotal, fill_max_mtotal, edgecolor='none', facecolor='k')
	#pylab.fill_betweenx(fill_mtotal, fill_min_mchirp, fill_max_mchirp, edgecolor='none', facecolor='0.2')
	#pylab.axvspan(1.1955, 1.2045, alpha=0.6, facecolor='white', edgecolor='k')

pylab.figure(figsize=(5,4), dpi=300)
pylab.gca().set_axis_bgcolor('#E6E6E6')
pylab.subplots_adjust(left=0.175, bottom=0.15)
pylab.xlim(0.5, 3)
pylab.ylim(2, 6)
#pylab.fill_between(fill_mchirp, fill_min_mtotal, fill_max_mtotal, edgecolor='k', facecolor='k')
foo()
#pylab.title(r'%d templates w/ component masses $1 \, \leqslant \, m/M_\odot \, \leqslant \, 3$' % n_big_templates)
pylab.xlabel(lloidplots.labels[column1])
pylab.ylabel(lloidplots.labels[column2])
#pylab.grid()

ax = pylab.gca()
ax.annotate(r'$1.1955 \, \leqslant \, \mathcal{M}/M_\odot \, \leqslant \, 1.2045$', xy=(1.225, 2.7), xycoords='data', xytext=(-10, -17), textcoords='offset points', arrowprops={'arrowstyle':'->'})
axins = zoomed_inset_axes(ax, 8, loc=7)
#pylab.plot(big_data[0], big_data[1], ',', color='0.6')
foo()
axins.set_ylim(2.7, 3.0)
axins.set_xlim(1.14, 1.26)
axins.get_xaxis().set_major_locator(ticker.MultipleLocator(0.05))
axins.get_yaxis().set_major_locator(ticker.MultipleLocator(0.1))
#axins.set_title('%d templates' % n_small_templates)
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.2")

pylab.savefig(sys.argv[1])
pylab.close()