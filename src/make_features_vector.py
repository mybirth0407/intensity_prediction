import peptide

fr = open('peptide_file1.tsv', 'rt', encoding='utf-8')

step = 1
fw = open('features_vector.txt', 'wt', encoding='utf-8')
for line in fr.readlines():
  print(step)
  l = line.split('\t')
  p = peptide.Peptide(l[9], l[8])
  fw.write(str(p.get_features()))
  fw.write('\n')
  step += 1
