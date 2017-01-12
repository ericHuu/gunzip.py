# -*- coding: utf-8 -*-
################################################################################
##  *
##  *  Function: Class and extract classed
##  *  Writer:Eric.Huu
##  *  Mail:erichu121@foxmail.com
##  *  QQ:185071180
##  *  Version:17.1.11
##  *  My motto: To make each script a usefultool!
##  *
################################################################################
#!/usr/bin/python
import os
from optparse import OptionParser

## help or usage or 
current_work_dir = os.getcwd()
usage = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nusage: %prog [options] args"
version = '%prog 17.1.11'
parser = OptionParser(usage=usage,version=version)
parser.add_option("-i","--input",action="store",
                  dest="input",
                  help="extract_from_fpkm.gtf(need to be class)[default:extract_from_fpkm.gtf]",
                  metavar = 'FILE',
                  default = 'extract_from_fpkm.gtf')               
parser.add_option("-d","--dir",action="store",
                  dest="workdir",
                  help="work dir/work path[default:current_work_dir]",
                  metavar = 'PATH',
                  default = current_work_dir+'/')
parser.add_option("-f","--gtf",action="store",
                  dest="gtf",
                  help="reference gtf[default:**/Sus_scrofa.Sscrofa10.2.81.gtf]",
                  metavar = 'FILE',
                  default = '/lustre/husilu/database/sus_scrofa/Sus_scrofa.Sscrofa10.2.81.gtf')
parser.add_option("-o","--out",action="store",
                  dest="out",
                  help="flag's for out[default:NA]",
                  metavar = 'STRING',
                  default = 'NA')
(options, args) = parser.parse_args()

os.system('''cd '''+str(options.workdir))
os.system('''FEELnc_classifier.pl -i '''+str(options.workdir)+str(options.input)+' -a '+str(options.gtf)+' > '+str(options.out)+'_classfied.txt')

intergenic=[]
transcript=[]
genic=[]
classed_file = str(options.out)+'_classfied.txt'
input_classfied = open(classed_file,"r")
output_total = open(str(options.out)+'_classes_total.txt',"w")

for line in input_classfied:
    line=line.strip()
    pa = line.split()
    if pa[2] not in transcript:
        transcript.append(pa[2])
    if line.startswith('1'):
        if pa[6]=='genic':
            genic.append(line)
        elif pa[6]=='intergenic':
            intergenic.append(line)
input_classfied.close()
print 'genic:',len(genic)
print 'intergenic:',len(intergenic)
print 'transcript:',len(transcript)

st=0
conver=0
diver=0
for line in intergenic:
    pa = line.split()
    if pa[8]=='same_strand':
        st+=1
    elif pa[8]=='convergent':
        conver+=1
    elif pa[8]=='divergent':
        diver+=1
print>>output_total,'intergenic\tsame_strand\t'+str(st)
print>>output_total,'intergenic\tconvergent\t'+str(conver)
print>>output_total,'intergenic\tdivergent\t'+str(diver)

over=[]
other=[]
for lines in genic:
    pa=lines.split()
    if pa[8]=='overlapping':
        over.append(lines)
    else:
        other.append(lines)
a=0
b=0
for line in over:
    pa = line.split()
    if pa[5]=='sense':
        a+=1
    else: ##### antisense
        b+=1
print>>output_total,'genic\toverlapping\tsense\t'+str(a)
print>>output_total,'genic\toverlapping\tantisense\t'+str(b)

c=0
d=0
e=0
f=0
for line in other:
    pa = line.split()
    if pa[5]=='sense' and pa[9]=='exonic':
        c+=1
    elif pa[5]=='antisense' and pa[9]=='intronic':
        d+=1
    elif pa[5]=='antisense' and pa[9]=='exonic':
        e+=1
    elif pa[5]=='sense' and pa[9]=='intronic':
        f+=1
print>>output_total,'genic\texonic\tsense\t'+str(c)
print>>output_total,'genic\texonic\tantisense\t'+str(e)
print>>output_total,'genic\tintronic\tsense\t'+str(f)
print>>output_total,'genic\tintronic\tantisense\t'+str(d)
output_total.close()

output_sense = open(str(options.out)+'_sense.xls',"w")
output_antisense = open(str(options.out)+'_antisense.xls',"w")
print>>output_sense,'sense'
print>>output_antisense,'antisense'
for line in open(classed_file,"r"):
	        line = line.lstrip().rstrip()
	        if line.startswith('isBEST'):
	            continue
	        pa = line.split('\t')
	        if pa[0] == '1':
	            if pa[5] == 'sense':
	                a = pa[2]
	                print>>output_sense,a
	            if pa[5] == 'antisense':
	                a = pa[2]
	                print>>output_antisense,a    
output_sense.close()
output_antisense.close()       


