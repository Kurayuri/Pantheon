#!/usr/bin/env python

import os
from os import path
from subprocess import check_call

import arg_parser
import context


def main():
    args = arg_parser.receiver_first()

    cc_repo = path.join(context.third_party_dir, 'aurora')
    src_dir = path.join(cc_repo, 'src')
    lib_dir = path.join(src_dir, 'core')
    app_dir = path.join(src_dir, 'app')
    send_src = path.join(app_dir, 'pccclient')
    recv_src = path.join(app_dir, 'pccserver')

    if args.option == 'setup':
        check_call(['make'], cwd=src_dir)
        return

    if args.option == 'receiver':
        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        cmd = [recv_src, 'recv', args.port]
        check_call(cmd)
        return

    if args.option == 'sender':
        os.environ['LD_LIBRARY_PATH'] = path.join(lib_dir)
        # cmd = [send_src, 'send', args.ip, args.port]

        # aurora
        cmd = [send_src, 'send', args.ip, args.port, 
            "--pcc-rate-control=python",
            "-pyhelper=loaded_client",
            "-pypath="+cc_repo+"/PCC-RL/src/udt-plugins/testing/",
            "--history-len=10",
            "--pcc-utility-calc=linear",
            "--model-path="+cc_repo+"/model/"+args.model
            # "--model-path=/home/kurayuri/pantheon/third_party/aurora/model/origin"
        ]
        print(" ".join(cmd))
        check_call(cmd)
        return


if __name__ == '__main__':
    main()
