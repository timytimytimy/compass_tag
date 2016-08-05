from fp_growth import find_frequent_itemsets
import re


proj_tags = dict()
proj_packages = dict()
packages = set()
pattern = re.compile("^([0-9a-zA-Z]+\.)+[0-9a-zA-Z]+$")

for line in open('tags').readlines():
    items = line.strip().split('\t')
    tags = items[1].strip().split(',')
    proj = items[0].strip()
    proj_tags[proj] = tags
    proj_packages[proj] = set()

for line in open('output_chat.csv').readlines():
    items = line.strip().split(',')
    proj = items[0].strip()
    package = items[3].strip()
    if proj_packages.has_key(proj):
        if pattern.match(package) is not None:
            proj_packages[proj].add(package)
            packages.add(package)

output_csv = open('model.csv', 'w')
pairs = list()

for proj in proj_tags.keys():
    obj = dict()
    obj['project'] = proj
    obj['tags'] = proj_tags[proj]
    obj['packages'] = list(proj_packages[proj])
    for tag in obj['tags']:
        for package in obj['packages']:
            if package.find('.'):
                pairs.append(['#%s#' % tag, package])

result_map = dict()
packages = sorted(list(packages))
line = ','.join(packages) + '\n'
output_csv.write(line)

for itemset in find_frequent_itemsets(pairs, 4):
    if len(itemset) > 1 and itemset[0].startswith('#'):
        if not result_map.has_key(itemset[0]):
            result_map[itemset[0]] = ['0' for p in packages]
        i = packages.index(itemset[1])
        result_map[itemset[0]][i] = '1'

for key in result_map.keys():
    line = '%s,%s\n' % (key.strip('#'), ','.join(result_map[key]))
    output_csv.write(line)