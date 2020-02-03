from Parsing1 import GenerateTruthTable as gtb, Parsing as ps

# Question 1
sentence_list = ps.open_txt("input.txt")
var_dic = ps.open_json("variables.json")
print("====== Question 1 ======")
for s in sentence_list:
    print(s+" ", end='')
print("= ", end='')
print(ps.parsing(sentence_list, var_dic))
print("========================\n")

num_of_var = 3  # set number of variables
sentence_list = ps.open_txt("input.txt")

print("=========== Question 2 ===========")
for s in sentence_list:
    print(s+" ", end='')
print()
gtb.generate_truth_table(sentence_list, num_of_var)
print("==================================")

