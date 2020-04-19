import pandas as pd
import numpy as np
import pylab as pl
from sklearn.metrics import roc_curve, auc
from sys import argv
df = pd.read_csv(argv[1])

y_test = np.array(df)[:,0]
probas = np.array(df)[:,1]

# Compute ROC curve and area the curve
fpr, tpr, thresholds = roc_curve(y_test, probas)
roc_auc = auc(fpr, tpr)
print("Area under the ROC curve : %f" % roc_auc)

# Plot ROC curve
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic')
pl.legend(loc="lower right")
pl.show()
