#!/bin/bash
#SBATCH --job-name=zeo++
#SBATCH --mail-type=ALL
#SBATCH --ntasks=16
#SBATCH --ntasks-per-socket=8
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2gb
#SBATCH --time=48:00:00


module purge

/blue/jsampath/alotmi.m/zeo/zeo++-0.3/./network -nor -nomass -psd 1.6 1.6 100000 system.psd *.cssr

/blue/jsampath/alotmi.m/zeo/zeo++-0.3/./network -nor -nomass -sa 1.6 1.6 100000 system.sa *.cssr

/blue/jsampath/alotmi.m/zeo/zeo++-0.3/./network -nor -nomass -vol 1.6 1.6 100000 system.vol *.cssr

