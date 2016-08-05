import numpy as np
import scipy.spatial.distance
from itertools import combinations, chain
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

def test():
    packages = set([line.strip() for line in open('test')])
    model = read_model()
    vector = np.array([1 if package in packages else 0 for package in model['_packages']])
    max_tag = ''
    max_r = 0
    for tags in model.keys():
        if tags != '_packages' and len(tags) > 1:
            r = scipy.spatial.distance.cosine(model[tags], vector)
            if r > max_r:
                 max_r, max_tag = r, tags
    print max_r, max_tag

if __name__ == '__main__':
    test()