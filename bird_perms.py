import csv

# manual input of all the names
# Got rid of the ones I've used for PII reasons!
# make sure the name lengths are multiples of 4, otherwise you won't find any solutions!
names = [
    "Jacob",
]

# I got my CSV from https://www.birdpop.org/docs/misc/IBPAOU.zip
# open up the CSV and save all the data
with open("IBP-Alpha-Codes20.csv", "r") as f:
    bird_csv_data = list(csv.DictReader(f))

# the SPEC column gives us the bird codes we need
codes = [bird["SPEC"] for bird in bird_csv_data]

# count each type of letter in the string
# I guess this works for any iterable, but whatever
def dist(string):
    # initialize the distribution with no occurences of each string
    d = {letter : 0 for letter in set(string)}
    # count all occurences
    for letter in string:
        d[letter] += 1
    return d

# get differences in occurences
# this will be used to see if the current list of bird codes we are using is wrong or incomplete
def dist_diff(dist1, dist2):
    sub = lambda x: (x, dist1.get(x, 0) - dist2.get(x, 0))
    keys = set(list(dist1) + list(dist2))
    return dict(map(sub, keys))


def all_birdmutations(name, current_codes=[]):
    # normalize to spec - AKA, remove all spaces and capitalize
    normalized_name = name.upper().replace(" ", "")
    name_dist = dist(normalized_name)
    # current_codes is a list of strings
    code_dist = dist("".join(current_codes))

    # take a diff to see how we are doing so far
    diff = dist_diff(name_dist, code_dist)
    # value < 0 means we have too many of at least one letter and we picked a bad bird code
    if any(value < 0 for value in diff.values()):
        pass
    # if we've made it this far, it could be that our diff is all 0s. that means we found a solution!
    elif all(value == 0 for value in diff.values()):
        yield current_codes
    # otherwise, our current_codes *might* lead to a solution and we should keep trying
    else:
        # we could just do "for code in codes:", but this is slow
        # we end up duplicating lots of work with situations like ["ABCD", "EFGH"] and ["EFGH", "ABCD"]
        # they are the same thing, but in different orders
        # instead, only pick codes that are alphabetically after the last one in current_codes

        # for newest_code we use " " as a default, because it is alphabetically before "a" and there are no " "'s in our codes!
        # therefore, it must always come first, meaning we don't filter anything out of the list
        newest_code = current_codes[-1] if len(current_codes) > 0 else " "
        not_checked = lambda code: code >= newest_code
        untried_codes = filter(not_checked, sorted(codes))
        for code in untried_codes:
            yield from all_birdmutations(name, current_codes=current_codes+[code])

for name in names:
    print(f"Name: {name}")
    birdmutations = list(all_birdmutations(name))
    if len(birdmutations) == 0:
        print("There are no solutions for this name")
    else:
        for birdmutation in birdmutations:
            print(birdmutation)
    print()
