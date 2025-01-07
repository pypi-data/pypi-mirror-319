# read version from installed package
from importlib.metadata import version
__version__ = version("pycounts_tat25")


from pycounts_tat25.pycounts_tat25 import count_words
from pycounts_tat25.plotting import plot_words