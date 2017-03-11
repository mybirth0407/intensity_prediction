import peptide

fr = [open('peptide_11_2_000.tsv', 'rt', encoding='utf-8'),
      open('peptide_11_2_001.tsv', 'rt', encoding='utf-8'),
      open('peptide_11_3_000.tsv', 'rt', encoding='utf-8'),
      open('peptide_11_3_001.tsv', 'rt', encoding='utf-8'),
      open('peptide_11_4_000.tsv', 'rt', encoding='utf-8'),
      open('peptide_11_4_001.tsv', 'rt', encoding='utf-8')]
fw = [open('features_vector_11_2_000.txt', 'wt', encoding='utf-8'),
      open('features_vector_11_2_001.txt', 'wt', encoding='utf-8'),
      open('features_vector_11_3_000.txt', 'wt', encoding='utf-8'),
      open('features_vector_11_3_001.txt', 'wt', encoding='utf-8'),
      open('features_vector_11_4_000.txt', 'wt', encoding='utf-8'),
      open('features_vector_11_4_001.txt', 'wt', encoding='utf-8')]

for i in range(6):
  step = 0
  for line in fr[i].readlines():
    if step == 100: break;
    l = line.split('\t')
    p = peptide.Peptide(l[9], l[8])
    fw[i].write(str(p.get_features()))
    fw[i].write('\n')
    step += 1
    print(step)
