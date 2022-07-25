#!/usr/bin/env python3

import argparse
import os
import gzip

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--infile",
        type=str
    )
    parser.add_argument(
        "--fastq_id",
        type=str
    )
    parser.add_argument(
        "--num_lines",
        type=int
    )
    parser.add_argument(
        "--kmer_size",
        type=int
    )
    parser.add_argument(
        "--lookahead",
        type=int
    )
    parser.add_argument(
        "--anchor_mode",
        type=str
    )
    parser.add_argument(
        "--window_slide",
        type=int
    )
    parser.add_argument(
        "--outfile",
        type=str
    )
    parser.add_argument(
        "--10X",
        action='store_true'
    )
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    if not args.10X:
        sample = args.fastq_id

    if args.anchor_mode == 'chunk':
        step_size = args.kmer_size
    elif args.anchor_mode == 'tile':
        step_size = args.window_slide

    x = 0

    file = gzip.open(args.outfile, 'wb')
    with gzip.open(args.infile, 'rt') as infile:
        for line in infile:
            if args.num_lines != 0:
                if x > args.num_lines:
                    break

            x += 1



            if x % 4 == 2:
                read = line.strip()

                last_base = len(read) - (args.lookahead + 2 * args.kmer_size)

                for i in range(0, last_base, step_size):
                    # get anchor
                    anchor = read[0+i : args.kmer_size+i]

                    # get target start and end positions, as a function of anchor end
                    target_start = (args.kmer_size+i) + args.lookahead
                    target_end = target_start + args.kmer_size

                    # get target
                    target = read[target_start : target_end]

                    if "N" not in anchor and "N" not in target:
                        file.write(str.encode(f'{anchor+target} {sample}\n'))
    file.close()


main()
