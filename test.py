import numpy as np
import scipy.spatial.distance
from itertools import combinations, chain
import re
allsubsets = lambda n: list(chain(*[combinations(n, ni) for ni in range(len(n) + 1)]))


def read_model():
    f = open('model.csv')
    model = dict()
    lines = f.readlines()
    model['_packages'] = lines[0].strip().split(',')
    tags = list()
    for line in lines[1:]:
        items = line.strip().split(',')
        model[items[0]] = [int(i) for i in items[1:]]
        tags.append(items[0])
    subsets = allsubsets(tags)
    ret = dict()
    ret['_packages'] = model['_packages']
    for subset in subsets:
        v = list()
        for i in xrange(len(model['_packages'])):
            x = 0
            for tag in subset:
                x |= model[tag][i]
            v.append(x)
        ret[subset] = np.array(v)
    return ret

def predict(project, packages):
    # packages = set([line.strip() for line in open('test')])
    if len(packages) == 0:
        return
    model = read_model()
    vector = np.array([1 if package in packages else 0 for package in model['_packages']])
    max_tag = ''
    max_r = 0
    for tags in model.keys():
        if tags != '_packages' and len(tags) > 1:
            r = scipy.spatial.distance.cosine(model[tags], vector)
            if r > max_r:
                 max_r, max_tag = r, tags
    print '%s,%s,%s' % (project, max_r, ','.join(max_tag))

def read_predict():
    pattern = re.compile("^([0-9a-zA-Z]+\.)+[0-9a-zA-Z]+$")
    f = open('test')
    last = ''
    packages = set()
    for line in f.readlines():
        items = line.strip().split(',')
        name = items[0].strip()
        package = items[1].strip()
        if last == name and pattern.match(package):
            packages.add(package)
        elif last != name:
            predict(last, packages)
            last = name
            packages = set()

if __name__ == '__main__':
    read_predict()