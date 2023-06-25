from sklearn.neural_network import MLPClassifier
import numpy, os, joblib

X, y = [], []


def extract_data():
    for file in os.listdir("."):
        if file.endswith(".npy"):
            X.append(numpy.load(file))
            y.append(file.split('_')[0])


extract_data()

# Settings use for mlp-demo.save
clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=100000, tol=1e-8, n_iter_no_change=10, verbose=True).fit(X, y)

# Faster but very bad
# clf = MLPClassifier().fit(X, y)

joblib.dump(clf, 'mlp.save')

