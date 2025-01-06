#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author: Zijie Jiang
@Contact: jzjlab@163.com
@File: test.py
@Time: 2024/12/26 13:52
@Function: main program entry
"""
import os


def main():
    hic = "/home/jzj/projects/PlotHiC/data/test.hic"
    chr_txt = "/home/jzj/projects/PlotHiC/data/chr.txt"
    # output = "test.png"
    output = "./"
    # plot_hic(hic, chr_txt=chr_txt, order=True, output=output, resolution=100000, bar_max=12,
    #          genome_name="PlotHiC-order", rotation=45, grid=True)
    # matrix = "/home/jzj/projects/PlotHiC/data/sample1_1000000.matrix"
    # abs_bed = "/home/jzj/projects/PlotHiC/data/sample1_1000000_abs.bed"
    # plot_bed(matrix, abs_bed, order_bed="", output=output, genome_name=None, fig_size=6, dpi=300,
    #          bar_min=0,
    #          bar_max=None, cmap="YlOrRd", log=False, rotation=45)

    if os.path.isdir(output):  # output is a directory
        print("Output is a directory")
    else:
        print("Output is a file")

if __name__ == '__main__':
    main()
