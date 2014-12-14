#!/usr/bin/python

import pickle
import sys

class Verb(object):
    def __init__(self, infinitiv, partizip_perfect, translation, success=0, tries=0):
        self.infinitiv = infinitiv
        self.partizip_perfect = partizip_perfect
        self.translation = translation
        self.success = success
        self.tries = tries

    def __str__(self):
        return "{infinitiv: %s, partizip_perfect: %s, translation: %s, %d/%d}" % (
                self.infinitiv,
                self.partizip_perfect,
                self.translation,
                self.success,
                self.tries)

    def __repr__(self):
        return self.__str__()

def load(text_file):
    with open(text_file, 'r') as fin:
        v = pickle.load(fin)
        print >>sys.stderr, "%d verbs were loaded from %s" % (len(v), text_file)
        return v

def save(verbs, text_file):
    if text_file:
        with open(text_file, 'w') as fin:
            pickle.dump(verbs, fin)
        print >>sys.stderr, "%d verbs were saved to %s" % (len(verbs), text_file)

def error(correct, x):
    print "Correct:", correct
    print "        ", x

    if len(correct) == len(x):
        a = [" " if correct[i] == x[i] else "^" for i in range(len(x))]
        print "        ",
        print "".join(a)


def ask(verb):
    print "%s" % verb.translation
    print "infinitiv:",
    infinitiv = raw_input().strip()
    print "Er ... ...",
    partizip_perfect = raw_input().strip()

    ok = True
    if infinitiv != verb.infinitiv:
        error(verb.infinitiv, infinitiv)
        ok = False
    if partizip_perfect != verb.partizip_perfect:
        error(verb.partizip_perfect, partizip_perfect)
        ok = False
    return ok

def run_test(verbs):
    v = list(verbs)
    v.sort(cmp=lambda x, y: int(x.success / (0.001 + x.tries) - y.success / (0.001 + y.tries)))
    w = c = 0
    for i in range(min(10, len(v))):
        r = ask(v[i])
        v[i].tries += 1
        v[i].success += r
        c += r
        w += 1

    print "Result is %d/%d" % (c, w)

def main():
    current_text_file = None
    verbs = set()

    while (True):
        print ">",
        s = raw_input()
        parts = s.split()
        if parts[0] == "init":
            save(verbs, current_text_file)

            verbs = set()
            current_text_file = parts[1]

        if parts[0] == "load":
            save(verbs, current_text_file)

            current_text_file = parts[1]
            verbs = load(current_text_file)
        if parts[0] == "save":
            assert current_text_file
            save(verbs, current_text_file)

        if parts[0] == "exit":
            save(verbs, current_text_file)
            break

        if parts[0] == "add":
            assert current_text_file
            print "\tinfinitiv:",
            infinitiv = raw_input()
            print "\tpartizip perfect:",
            partizip_perfect = raw_input()
            if not (partizip_perfect.startswith("hat") or partizip_perfect.startswith("bin")):
                print "Did you forget 'hat'?(y)",
                y = raw_input()
                if y == "y":
                    partizip_perfect = "hat %s" % partizip_perfect
                    print "Ok, adding '%s'" % partizip_perfect

            print "\ttranslation:",
            translation = raw_input()
            verbs.add(Verb(infinitiv.strip(), partizip_perfect.strip(), translation.strip()))
            print verbs

        if parts[0] == "test":
            run_test(verbs)
            save(verbs, current_text_file)
        if parts[0] == "print":
            print verbs
        if parts[0] == "edit":
            for (i,v) in enumerate(verbs):
                print "\t%d, %s" %(i,v)
            print "Enter number of a verb to edit: >",
            number = int(raw_input())
            v_e = list(verbs)[number]
            for a in ['infinitiv', 'partizip_perfect', 'translation']:
                print "New value for %s(old value %s): /leave empty to not change/:>" % (
                        a, v_e.__getattribute__(a)),
                s = raw_input().strip()
                if s:
                    v_e.__setattr__(a, s)
            print "Result: ", v_e



    print >>sys.stderr, "Exiting..."

    '''if sys.argv[1] == "init":

    if sys.argv[1] == "load":
        verbs = load(sys.argv[1])
        print verbs'''

main()
