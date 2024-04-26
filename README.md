Overview
========

This project contains examples of pytests that we've found useful to integrate into customer CICD pipelines. All tests are stored in the tests folder, and have a brief description below.

Project Contents
================

### test_dag_parse_time.py
This test uses dagbag.process_file() to determine how long each dag is taking to parse. Any dag that exceeds an arbitrary time limit (5 seconds in the example) are considered to have failed, and their parsing time is output.

### test_operator_blacklist.py
This actually contains two related tests. operator_list.json contains operators and their status (blacklisted, whitelisted, or deprecated). Dags are tested to see whether they comply with whitelist or blacklist policies, and fail if they do not. Operators that fall outside the policy boundaries are included in the test failure output. These lists are also enforced via cluster policies in cluster_policies.py