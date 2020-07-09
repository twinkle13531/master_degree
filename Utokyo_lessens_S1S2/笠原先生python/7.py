
import sys
read_lines=sys.stdin.readlines()
for i, read_line in enumerate(read_lines):
  if i>=192 and i<=253:
    if "<li><a href=" in read_line:
      if "sequence_only" not in read_line:

        read_line2=read_line.split('>')
        #print(read_line2)
        mammal_name=read_line2[2].replace("</a", "").strip()
        #print(read_line2[2])
        print(mammal_name)

