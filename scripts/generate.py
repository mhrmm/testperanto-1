import argparse
import json
import sys
from tqdm import tqdm
from testperanto.macros import TreeTransducer, init_transducer_cascade
from testperanto.macros import run_transducer_cascade
from testperanto.trees import TreeNode, LeafLabelCollector
from testperanto.voicebox import VoiceboxFactory


def main(config_files, switching_code, num_to_generate, only_sents):
    cascade = init_transducer_cascade(config_files, switching_code)
    for _ in tqdm(range(num_to_generate)):
        output = run_transducer_cascade(cascade)
        if only_sents:
            collector = LeafLabelCollector()
            collector.execute(output)
            leaves = ['~'.join(leaf) for leaf in collector.get_leaf_labels()]
            leaves = [leaf for leaf in leaves if leaf != "NULL"]
            output = ' '.join(leaves)
        print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate trees using testperanto.')
    parser.add_argument('-c', '--configs', nargs='+', required=True,
                        help='names of the transducer config files in the cascade')
    parser.add_argument('-n', '--num', required=True, type=int,
                        help='number of trees to generate')
    parser.add_argument('-s', '--switches', required=False, default=None,
                        help='the typological switches, as a bitstring')
    parser.add_argument('--sents', dest='sents', action='store_true', default=False,
                        help='only output sentences (rather than trees)')
    args = parser.parse_args()
    main(args.configs, args.switches, args.num, args.sents)
