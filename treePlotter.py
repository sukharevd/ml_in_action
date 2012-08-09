#######################################################################
# This is unfinished and not working example of plotting decision tree
# from page 50 of ML in Action. I just think that it isn't worth to 
# spent time visualizing decision tree with tool that isn't optimazed
# for this purpose. Moreover JSON-like decistion tree is quite readable
# as for me.
#######################################################################

import matplotlib.pyplot as plot

decisionNode = dict(boxstyle = 'sawtooth', fc = '0.8')
leafNode = dict(boxstyle = 'round4', fc = '0.8')
arrowArgs = dict(arrowstyle = '<-')

def plotNode(nodeText, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeText, xy=parentPt, xycoords='axes fracton',
    xytext=centerPt, textcoords='axes fraction', va='center', ha='center',
    bbox=nodeType, arrowprops=arrowArgs)

def createPlot():
    fig = plot.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plot.subplot(111, frameon=False)
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plot.show()

createPlot()
