# -*- coding: utf-8 -*-

# Title: spec2k6_simple_cache
# Author: Conor Green
# Purpose: Final Project for ECE565
# Description: Modification of spec2k6 script which helps parse 
#       which benchmark and creates a process. Heavily based on
#       Melek Musleh's spec2k6 code: the copyright is given below.
# Usage: Call through get_process() from another script (simple_cache_benchmarking)


# Copyright (c) 2012 Purdue University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Malek Musleh

### The following file was referenced from the following site:
### http://www.m5sim.org/SPEC_CPU2006_benchmarks
###
### and subsequent changes were made


import os
import optparse
import sys

import m5
from m5.objects import *



def get_process(options):
    process = Process()
    if options.benchmark == 'perlbench':
       process = perlbench
    elif options.benchmark == 'bzip2':
       process = bzip2
    elif options.benchmark == 'gcc':
       process = gcc
    elif options.benchmark == 'bwaves':
       process = bwaves
    elif options.benchmark == 'gamess':
       process = gamess
    elif options.benchmark == 'mcf':
       process = mcf
    elif options.benchmark == 'milc':
       process = milc
    elif options.benchmark == 'zeusmp':
       process = zeusmp
    elif options.benchmark == 'gromacs':
       process = gromacs
       shutil.copy(os.path.join(process.cwd,"gromacs.tpr"),os.getcwd())
    elif options.benchmark == 'cactusADM':
       process = cactusADM
    elif options.benchmark == 'leslie3d':
       process = leslie3d
    elif options.benchmark == 'namd':
       process = namd
    elif options.benchmark == 'gobmk':
       process = gobmk;
    elif options.benchmark == 'dealII':
       process = dealII
    elif options.benchmark == 'soplex':
       process = soplex
    elif options.benchmark == 'povray':
       process = povray
    elif options.benchmark == 'calculix':
       process = calculix
    elif options.benchmark == 'hmmer':
       process = hmmer
    elif options.benchmark == 'sjeng':
       process = sjeng
    elif options.benchmark == 'GemsFDTD':
       process = GemsFDTD
    elif options.benchmark == 'libquantum':
       process = libquantum
    elif options.benchmark == 'h264ref':
       process = h264ref
    elif options.benchmark == 'tonto':
       process = tonto
    elif options.benchmark == 'lbm':
       process = lbm
    elif options.benchmark == 'omnetpp':
       process = omnetpp
    elif options.benchmark == 'astar':
       process = astar
    elif options.benchmark == 'wrf':
       process = wrf
    elif options.benchmark == 'sphinx3':
       process = sphinx3
    elif options.benchmark == 'xalancbmk':
       process = xalancbmk
    elif options.benchmark == 'specrand_i':
       process = specrand_i
    elif options.benchmark == 'specrand_f':
       process = specrand_f
    return process


m5.util.addToPath('../common')

bench_dir='/home/min/a/ece565/benchspec-2020/CPU2006/'
### Note: That some benchmarks require this variable to be modified to match
### your home environment. This variable only applies for certain benchmarks
### that require read/write to an output directory
output_dir= '/home/min/a/$USER/outputs/spec2k6/'

if buildEnv['TARGET_ISA'] == 'arm':
    benchtype = "-armcross"
elif buildEnv['TARGET_ISA'] == 'x86':
    benchtype = '-m64-gcc43-nn'
else:
    sys.exit("Unsupported ISA")

#400.perlbench
perlbench = Process()
perlbench_dir = '400.perlbench/'
perlbench.executable =  bench_dir+perlbench_dir+\
    '/run/perlbench_base.amd64' + benchtype

perlbench.cmd = [perlbench.executable] +\
    ['-I./lib', 'checkspam.pl', '2500', '5', '25',\
    '11', '150', '1', '1', '1', '1' ]
perlbench.cwd = bench_dir+perlbench_dir+'/run/'
perlbench.output = 'attrs.out'

#401.bzip2
bzip2 = Process()
bzip2_dir = '401.bzip2/'
bzip2.executable =  bench_dir+bzip2_dir+\
    '/exe/bzip2_base.amd64' + benchtype
data=bench_dir+bzip2_dir+'data/ref/input/input.source'
bzip2.cmd = [bzip2.executable] + [data, '1']
bzip2.output = 'input.source.out'

#403.gcc
gcc = Process()
gcc_dir = '403.gcc/'
gcc.executable =  bench_dir+gcc_dir+\
    '/exe/gcc_base.amd64' + benchtype
data=bench_dir+'/data/ref/input/166.i'
output=output_dir+'/gcc/166.s'
gcc.cmd = [gcc.executable] + [data]+['-o',output] + ['-quiet'] \
+ ['-funroll-loops'] + ['-fforce-mem'] + ['-fcse-follow-jumps'] \
+ ['-fcse-skip-blocks'] + ['-fexpensive-optimizations'] \
+ ['-fstrength-reduce'] + ['-fpeephole']  + ['-fschedule-insns'] \
+ ['-finline-functions'] + ['-fschedule-insns2']

#410.bwaves
bwaves = Process()
bwaves_dir=bench_dir+'/410.bwaves'
bwaves.executable =  bwaves_dir+'/run/bwaves_base.amd64' + benchtype
bwaves.cwd = bwaves_dir+'/run/'
bwaves.cmd = [bwaves.executable]

#416.gamess
gamess=Process()
gamess_dir='416.gamess/'
gamess.executable =  bench_dir+gamess_dir+\
    '/run/gamess_base.amd64' + benchtype
gamess.cmd = [gamess.executable] + ['cytosine.2.config']
gamess.cwd = bench_dir+gamess_dir+'/run'
gamess.output='cytosine.2.output'

#429.mcf
mcf = Process()
mcf_dir = '429.mcf/'
mcf.executable = bench_dir+mcf_dir+\
    '/exe/mcf_base.amd64' + benchtype
data=bench_dir+mcf_dir+'/data/ref/input/inp.in'
mcf.cmd = [mcf.executable] + ['inp.in']
mcf.cwd = bench_dir+mcf_dir+'/run/'
mcf.output = 'inp.out'

#433.milc
milc=Process()
milc_dir='433.milc/'
milc.executable = bench_dir+milc_dir+\
    '/exe/milc_base.amd64' + benchtype
stdin=bench_dir+milc_dir+'/data/ref/input/su3imp.in'
milc.cmd = [milc.executable]
milc.input=stdin
milc.output='su3imp.out'

#434.zeusmp
zeusmp=Process()
zeusmp_dir='434.zeusmp/'
zeusmp.executable = bench_dir+zeusmp_dir+\
    '/run/zeusmp_base.amd64' + benchtype
zeusmp.cmd = [zeusmp.executable]
zeusmp.cwd = bench_dir+zeusmp_dir+'/run'
zeusmp.output = 'zeusmp.stdout'

#435.gromacs
gromacs = Process()
gromacs_dir='435.gromacs/'
gromacs.executable = bench_dir+gromacs_dir+\
    '/run/gromacs_base.amd64' + benchtype
data=os.getcwd()+'/gromacs.tpr'
gromacs.cwd = bench_dir+gromacs_dir+'/run'
gromacs.cmd = [gromacs.executable] + ['-silent','-deffnm',data,'-nice','0']

#436.cactusADM
cactusADM = Process()
cactusADM_dir = '436.cactusADM/'
cactusADM.executable =  bench_dir+cactusADM_dir+\
    '/run/cactusADM_base.amd64' + benchtype
data=bench_dir+cactusADM_dir+'/data/ref/input/benchADM.par'
cactusADM.cmd = [cactusADM.executable] + ['benchADM.par']
cactusADM.cwd = bench_dir+cactusADM_dir + '/run'
cactusADM.output = 'benchADM.out'

#437.leslie3d
leslie3d=Process()
leslie3d_dir= '437.leslie3d/'
leslie3d.executable = bench_dir+leslie3d_dir+\
    '/exe/leslie3d_base.amd64' + benchtype
stdin=bench_dir+leslie3d_dir+'/data/ref/input/leslie3d.in'
leslie3d.cmd = [leslie3d.executable]
leslie3d.input=stdin
leslie3d.output='leslie3d.stdout'

#444.namd
namd = Process()
namd_dir='444.namd/'
namd.executable =  bench_dir+namd_dir+\
    '/exe/namd_base.amd64' + benchtype
input=bench_dir+namd_dir+'/data/all/input/namd.input'
namd.cmd = [namd.executable] + ['--input',input,'--iterations','1',\
    '--output','namd.out']
namd.output='namd.stdout'

#445.gobmk
gobmk=Process()
gobmk_dir = '445.gobmk/'
gobmk.executable = bench_dir+gobmk_dir+\
    '/exe/gobmk_base.amd64' + benchtype
stdin=bench_dir+gobmk_dir+'/data/ref/input/13x13.tst'
gobmk.cmd = [gobmk.executable]+['--quiet','--mode','gtp']
gobmk.input=stdin
gobmk.output='capture.out'

#447.dealII
dealII=Process()
dealII_dir = '447.dealII/'
dealII.executable = bench_dir+dealII_dir+\
    '/exe/dealII_base.amd64' + benchtype
dealII.cmd = [gobmk.executable]+['8']
dealII.output='log'

#450.soplex
soplex=Process()
soplex_dir = '450.soplex/'
soplex.executable = bench_dir+soplex_dir+\
    '/run/soplex_base.amd64' + benchtype
data=bench_dir+soplex_dir+'/data/ref/input/ref.mps'
soplex.cmd = [soplex.executable]+['-m10000','ref.mps']
soplex.cwd = bench_dir+soplex_dir+"/run/"
soplex.output = 'test.out'

#453.povray
povray=Process()
povray_dir = '453.povray/'
povray.executable = bench_dir+povray_dir+\
    '/exe/povray_base.amd64' + benchtype
data=bench_dir+povray_dir+'/data/ref/input/SPEC-benchmark-ref.ini'
povray.cmd = [povray.executable]+[data]
povray.output = 'SPEC-benchmark-ref.stdout'

#454.calculix
calculix=Process()
calculix_dir='454.calculix/'
calculix.executable = bench_dir+calculix_dir+\
    '/exe/calculix_base.amd64' + benchtype
data='/data/ref/input/hyperviscoplastic.inp'
calculix.cmd = [calculix.executable]+['-i',data]
calculix.output = 'beampic.log'

#456.hmmer
hmmer=Process()
hmmr_dir = '456.hmmer/'
hmmer.executable = bench_dir+hmmr_dir+\
    '/exe/hmmer_base.amd64' + benchtype
data=bench_dir+hmmr_dir+'/data/ref/input/nph3.hmm'
hmmer.cmd = [hmmer.executable]+['--fixed', '0', '--mean', '325',\
    '--num', '5000', '--sd', '200', '--seed', '0', data]
hmmer.output = 'bombesin.out'

#458.sjeng
sjeng=Process()
sjeng_dir = '458.sjeng/'
sjeng.executable =  bench_dir+sjeng_dir+\
    '/exe/sjeng_base.amd64' + benchtype
data=bench_dir+sjeng_dir+'/data/ref/input/ref.txt'
sjeng.cmd = [sjeng.executable]+[data]
sjeng.output = 'ref.out'

#459.GemsFDTD
GemsFDTD=Process()
GemsFDTD_dir = '459.GemsFDTD/'
GemsFDTD.executable =  bench_dir+GemsFDTD_dir+\
    '/exe/GemsFDTD_base.amd64' + benchtype
GemsFDTD.cmd = [GemsFDTD.executable]
GemsFDTD.output = 'ref.log'

#462.libquantum
libquantum=Process()
libquantum_dir ='462.libquantum/'
libquantum.executable = bench_dir+libquantum_dir+\
    '/exe/libquantum_base.amd64' + benchtype
libquantum.cmd = [libquantum.executable],'33','5'
libquantum.output = 'ref.out'

#464.h264ref
h264ref=Process()
h264_dir = '464.h264ref/'
h264ref.executable = bench_dir+h264_dir+\
    '/run/h264ref_base.amd64' + benchtype
data=bench_dir+h264_dir+'/data/ref/input/foreman_ref_encoder_baseline.cfg'
h264ref.cmd = [h264ref.executable]+['-d',data]
h264ref.cwd = bench_dir+h264_dir+'/run'
h264ref.output = 'foreman_ref_encoder_baseline.out'

#465.tonto
tonto=Process()
tonto_dir = '465.tonto/'
tonto.executable = bench_dir+tonto_dir+\
    '/run/tonto_base.amd64' + benchtype
data=bench_dir+tonto_dir+'/data/ref/input/foreman_ref_encoder_baseline.cfg'
tonto.cmd = [tonto.executable]
tonto.cwd = bench_dir+tonto_dir+'/run'
tonto.output = 'tonto.out'

#470.lbm
lbm=Process()
lbm_dir='470.lbm/'
lbm.executable = bench_dir+lbm_dir+'/exe/lbm_base.amd64' + benchtype
data=bench_dir+lbm_dir+'/data/ref/input/100_100_130_ldc.of'
lbm.cmd = [lbm.executable]+['20', 'reference.dat', '0', '1' ,data]
lbm.output = 'lbm.out'

#471.omnetpp
omnetpp=Process()
omnetpp_dir = '471.omnetpp/'
omnetpp.executable =  bench_dir+omnetpp_dir+\
    '/exe/omnetpp_base.amd64' + benchtype
data=bench_dir+omnetpp_dir+'/data/ref/input/omnetpp.ini'
omnetpp.cmd = [omnetpp.executable]+[data]
omnetpp.output = 'omnetpp.log'

#473.astar
astar=Process()
astar_dir='473.astar'
astar.executable = bench_dir+astar_dir+\
    '/run/astar_base.amd64' + benchtype
data=bench_dir+astar_dir+'/data/ref/input/rivers.cfg'
astar.cmd = [astar.executable]+[data]
astar.cwd = bench_dir+astar_dir+'/run'
astar.output = 'lake.out'

#481.wrf
wrf=Process()
wrf_dir = '481.wrf'
wrf.executable = bench_dir+wrf_dir+'/exe/wrf_base.amd64' + benchtype
data = bench_dir+wrf_dir+'/data/ref/input/namelist.input'
wrf.cmd = [wrf.executable]+[data]
wrf.output = 'rsl.out.0000'

#482.sphinx
sphinx3=Process()
sphinx3_dir = '482.sphinx3'
sphinx3.executable =  bench_dir+sphinx3_dir+\
    '/run/sphinx_livepretend_base.amd64' + benchtype
sphinx3.cmd = [sphinx3.executable]+['ctlfile', '.', 'args.an4']
sphinx3.cwd = bench_dir+sphinx3_dir + '/run/'
sphinx3.output = 'an4.out'

#483.xalancbmk
xalancbmk=Process()
xalanch_dir = '483.xalancbmk/'
xalancbmk.executable =  bench_dir+xalanch_dir+\
    '/run/Xalan_base.amd64' + benchtype
data = bench_dir + xalanch_dir + '/data/ref/input/'
xalancbmk.cmd = [xalancbmk.executable]+['-v','t5.xml','xalanc.xsl']
xalancbmk.cwd = bench_dir+xalanch_dir+'/run'
xalancbmk.output = 'ref.out'

#998.specrand
specrand_i=Process()
specrand_i_dir = '998.specrand/'
specrand_i.executable = bench_dir+specrand_i_dir+\
    '/run/specrand_base.amd64' + benchtype
specrand_i.cmd = [specrand_i.executable] + ['324342','24239']
specrand_i.cwd = bench_dir+specrand_i_dir+'/run'
specrand_i.output = 'rand.24239.out'

#999.specrand
specrand_f=Process()
specrand_f_dir = '999.specrand/'
specrand_f.executable = bench_dir+specrand_f_dir+\
    '/run/specrand_base.amd64' + benchtype
specrand_f.cmd = [specrand_f.executable] + ['324342','24239']
specrand_f.cwd = bench_dir+specrand_f_dir+'/run'
specrand_f.output = 'rand.24239.out'
