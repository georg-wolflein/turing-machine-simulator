#!/usr/bin/env python3

import subprocess
import os
from glob import glob

TEST_DIR = "."
SRC_DIR = os.path.join("..", "src")
RUNTM = os.path.join(SRC_DIR, "runtm")

TEST_TYPES = {
    "accept": 0,
    "reject": 1
}

NULL = open(os.devnull, "w")

print("Running make...")
subprocess.run(["make", "-C", SRC_DIR], stdout=NULL)

num_tests = 0
passed_tests = 0

for tm in os.listdir(TEST_DIR):
    for tmfile in glob(os.path.join(SRC_DIR, tm + "*.tm")):
        print("Running {} tests on {}...".format(tm, tmfile))
        for test_type, returncode in TEST_TYPES.items():
            for tape in sorted(glob(os.path.join(TEST_DIR, tm, test_type, "*.tape"))):
                result = subprocess.run(
                    [RUNTM, tmfile, tape], stdout=subprocess.PIPE)
                passed = result.returncode == returncode
                reason = "incorrect return code"
                if passed:
                    if os.path.exists(tape + "out"):
                        with open(tape + "out") as f:
                            passed = result.stdout.decode(
                                "utf-8").strip().split("\n")[-1].strip() == f.read().strip()
                            reason = "incorrect tape output"
                if passed:
                    print("  \033[92mPASS\033[0m {}".format(tape))
                    passed_tests += 1
                else:
                    print("  \033[91mFAIL\033[0m {} ({})".format(tape, reason))
                num_tests += 1

print()
print("Summary:")
print("  {} out of {} tests passed".format(passed_tests, num_tests))
