from aagam_packages.terminal_yoda.terminal_yoda import *

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(yoda_saberize(YodaSaberColor.DARKGREEN) + tf.__version__)