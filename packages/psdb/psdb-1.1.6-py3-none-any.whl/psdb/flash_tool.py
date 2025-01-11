#!/usr/bin/env python3
# Copyright (c) 2018-2019 Phase Advanced Sensor Systems, Inc.
import argparse
import hashlib
import time
import sys

import psdb.probes
import psdb.elf
import psdb.hexfile


IMAGE_PARSERS = [psdb.elf.ELFBinary.from_path,
                 psdb.hexfile.HEXFile,
                 ]


def parse_image(path):
    for ip in IMAGE_PARSERS:
        try:
            return ip(path)
        except Exception:
            pass

    raise Exception('Unrecognized file type.')


def main(rv):  # noqa: C901
    # Dump all debuggers if requested.
    if rv.dump_debuggers:
        psdb.probes.dump_probes()
        return

    # Probe the specified serial number (or find the default if no serial number
    # was specified.
    probe = psdb.probes.make_one_ns(rv)

    # SRST the target, if requested.  We have to assert this for at least 1 us.
    if rv.srst:
        probe.srst_target()

    # Use the probe to detect a target platform.
    f = probe.set_tck_freq(rv.probe_freq)
    print('Probing with SWD frequency at %.3f MHz' % (f/1.e6))
    target = probe.probe(verbose=rv.verbose,
                         connect_under_reset=rv.connect_under_reset)
    f      = probe.set_max_target_tck_freq()
    print('Set SWD frequency to %.3f MHz' % (f/1.e6))

    # Flash info if verbose.
    if rv.verbose:
        print('       Flash size: %u' % target.flash.flash_size)
        print('Flash sector size: %u' % target.flash.sector_size)

    # Read a backup of flash if requested.
    if rv.read_flash:
        t0 = time.time()
        data = target.flash.read_all()
        dt = time.time() - t0
        with open(rv.read_flash, 'wb') as f:
            f.write(data)
        md5 = hashlib.md5(data)
        print('Read %u bytes in %.2f seconds (%.2f K/s).'
              % (len(data), dt, len(data) / (1024*dt)))
        print('MD5: %s' % md5.hexdigest())

    # Dump options if requested.
    if rv.get_options or rv.option:
        print('Initial options: 0x%08X' % target.flash.get_options_reg())
        print(target.flash.get_options())

    # Option bytes if requested.
    if rv.option:
        options = {k.lower() : int(v, 0) for k, v in rv.option}
        target = target.flash.set_options(options, verbose=rv.verbose,
                                          connect_under_reset=True)
        print('Final options: 0x%08X' % target.flash.get_options_reg())
        final_opts = target.flash.get_options()
        print(final_opts)
        for k, v in options.items():
            if final_opts[k] != v:
                print('Warning: option "%s" is %u not %u.'
                      % (k, final_opts[k], v))

    # Erase the flash if requested.
    if rv.erase:
        target.flash.erase_all()
        target.reset_halt()

    # Erase individual regions if requested.
    if rv.erase_region:
        for r in rv.erase_region:
            base, length = r.split(',')
            base         = int(base, 0)
            length       = int(length, 0)
            target.flash.erase(base, length, verbose=True)

    # Write a new ELF image to flash if requested.
    if rv.flash:
        dv = []
        for path in rv.flash:
            print('Burning "%s"...' % path)
            with open(path, 'rb') as f:
                md5 = hashlib.md5(f.read())
            print('MD5: %s' % md5.hexdigest())
            img = parse_image(path)
            pdv = target.flash.prune_dv(img.flash_dv)
            dv  = psdb.elf.dv.merge_dvs(dv, pdv)
        target.flash.burn_dv(dv, verbose=True, bank_swap=rv.flash_inactive)
        print('Flash completed successfully.')
        target.reset_halt()

    # Write a raw binary file to flash if requested.
    if rv.write_raw_binary:
        print('Burning "%s"...' % rv.write_raw_binary)
        with open(rv.write_raw_binary, 'rb') as f:
            data = f.read()
        target.flash.burn_dv([(target.flash.mem_base, data)],
                             verbose=True, bank_swap=rv.flash_inactive)
        print('Flash completed successfully.')
        target.reset_halt()

    # Dump some memory.
    if rv.mem_dump:
        print('Memory dump:')
        base, length = rv.mem_dump.split(',')
        base         = int(base, 0)
        length       = int(length, 0)
        mem          = target.cpus[0].read_bulk(base, length)
        psdb.hexdump(mem, addr=base)

    # If bank-swapping was requested, do it now.  Otherwise, resume if
    # requested.
    if rv.swap_banks:
        target.flash.swap_banks_and_reset_no_connect()
        if rv.halt:
            target = target.reprobe(connect_under_reset=True)
        if not rv.flash_inactive:
            if rv.flash or rv.write_raw_binary:
                print('*****************************************************')
                print('Warning: --flash-inactive should be used when trying')
                print('to write to the peer bank and activate it.')
                print('You just wrote to what was the currently-active bank')
                print('and then activated the previously-inactive bank which')
                print('probably isn\'t what you wanted.')
                print('*****************************************************')
    elif not rv.halt:
        target.resume()


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump-debuggers', '-d', action='store_true')
    parser.add_argument('--usb-path')
    parser.add_argument('--serial-num')
    parser.add_argument('--halt', action='store_true')
    parser.add_argument('--srst', action='store_true')
    parser.add_argument('--connect-under-reset', action='store_true')
    parser.add_argument('--read-flash')
    parser.add_argument('--flash', action='append')
    parser.add_argument('--write-raw-binary')
    parser.add_argument('--flash-inactive', action='store_true')
    parser.add_argument('--erase', action='store_true')
    parser.add_argument('--erase-region', action='append')
    parser.add_argument('--mem-dump', '-m')
    parser.add_argument('--probe-freq', type=int, default=1000000)
    parser.add_argument('--max-tck-freq', type=int)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--swap-banks', action='store_true')
    parser.add_argument('--get-options', action='store_true')
    parser.add_argument('--option', '-o', nargs=2, action='append')
    rv = parser.parse_args()

    try:
        main(rv)
    except psdb.ProbeException as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    _main()
