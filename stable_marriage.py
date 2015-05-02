import json
import sys
import copy
import argparse

# parse arguments from command line
parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [-m]/[-w] <inputfile> -o <outputfile>', description='Stable marriage solver')
parser.add_argument('-m', action='store_true', required=False)
parser.add_argument('-w', action='store_true', required=False)
parser.add_argument('inputfile')
parser.add_argument("-o", "--output", help="Directs the output to a name of your choice")

args = parser.parse_args()

# open input file
file1 = args.inputfile
f = open(file1, 'r')
j = json.load(f)
f.close()

# create list for men from json file
men_list = j["men_rankings"]
guys = sorted(men_list.keys())

# create list for women from json file
women_list = j["women_rankings"]
girls = sorted(women_list.keys())

# function tha solves the problem for men
def men_GS_matcher():
    free_men = guys[:]
    married = {}
    men_priorities = copy.deepcopy(men_list)
    women_priorities = copy.deepcopy(women_list)
    while free_men:
        guy = free_men.pop(0)
        guyslist = men_priorities[guy]
        girl = guyslist.pop(0)
        fiance = married.get(girl)
        if not fiance:
            # She's free
            married[girl] = guy
            # print("  %s and %s" % (guy, girl))
        else:
            # proposal to a married girl
            girllist = women_priorities[girl]
            if girllist.index(fiance) > girllist.index(guy):
                married[girl] = guy
                if men_priorities[fiance]:
                    free_men.append(fiance)
            else:
                 # She is faithful to old fiance
                if guyslist:
                    # Look again
                    free_men.append(guy)
    return married

# function tha solves the problem for women
def women_GS_matcher():
    free_women = girls[:]
    married = {}
    women_priorities = copy.deepcopy(women_list)
    men_priorities = copy.deepcopy(men_list)
    while free_women:
        girl = free_women.pop(0)
        girlslist = women_priorities[girl]
        guy = girlslist.pop(0)
        fiance = married.get(guy)
        if not fiance:
            married[guy] = girl
            # print("  %s and %s" % (girl, guy))
        else:
            guylist = men_priorities[guy]
            if guylist.index(fiance) > guylist.index(girl):
                married[guy] = girl
                if women_priorities[fiance]:
                    free_women.append(fiance)
            else:
                if girlslist:
                    free_women.append(girl)
    return married

if args.m:
    # produce JSON for men optimal or write json to output file
    if len(sys.argv) == 3:
        engaged = men_GS_matcher()
        new_dict = dict (zip(engaged.values(),engaged.keys()))
        json_string = json.dumps(new_dict,sort_keys=True, indent=4)
        print(json_string)
    elif len(sys.argv) == 5:
        file2 = args.output
        f2 = open(file2, 'w')
        f2.close()
        sys.stdout = open(file2, 'w')
        engaged = men_GS_matcher()
        new_dict = dict (zip(engaged.values(),engaged.keys()))
        json_string = json.dumps(new_dict,sort_keys=True, indent=4)
        print(json_string)
elif args.w:
    #  produce JSON for women optimal or write json to output file
    if len(sys.argv) == 3:
        engaged = women_GS_matcher()
        new_dict = dict(zip(engaged.values(), engaged.keys()))
        json_string = json.dumps(new_dict,sort_keys=True, indent=4)
        print(json_string)
    elif len(sys.argv) == 5:
        file2 = args.output
        f2 = open(file2, 'w')
        f2.close()
        sys.stdout = open(file2, 'w')
        engaged = women_GS_matcher()
        new_dict = dict (zip(engaged.values(),engaged.keys()))
        json_string = json.dumps(new_dict,sort_keys=True, indent=4)
        print(json_string)