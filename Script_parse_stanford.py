"""Python script to syntactically parse a sentence with the Stanford Parser
Available from https://nlp.stanford.edu/software/lex-parser.shtml
Earl Kjar Brown, ekbrown byu edu (add appropriate characters to create email)
"""

# specify your sentence here
sent = "I wonder how this thing works."

# specify the pathway to the directory with the Stanford Parser
pathdir_stan_parser = "/Users/ekb5/Documents/stanford-parser-full-2018-10-17"

import nltk, os, subprocess
from nltk.draw.tree import TreeView

os.chdir(pathdir_stan_parser)
with open("temp.txt", "w", encoding = "utf8") as outfile:
    outfile.write(sent)
to_cmd = f'java -mx200m -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "penn" englishPCFG.ser.gz temp.txt'

# take the parsed sentence
output = subprocess.run(to_cmd, shell = True, stdout = subprocess.PIPE)
to_str = output.stdout.decode("utf8")
print(to_str)

# draw it to the console
tree = nltk.Tree.fromstring(to_str)
tree.pretty_print()

# write prettier tree to a PostScript file
TreeView(tree)._cframe.print_to_file('output.ps')
