#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2011-2013.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

"""
 @example use_debug_layers.cpp

 Simple example showing how to use some of the debug layers defined
 in Kodo.
"""

import os
import random

import kodo


def main():
    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 8
    symbol_size = 16

    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders
    encoder_factory = kodo.full_rlnc_encoder_factory_binary8_trace(symbols,
                                                                   symbol_size)
    encoder = encoder_factory.build()

    decoder_factory = kodo.full_rlnc_decoder_factory_binary8_trace(symbols,
                                                                   symbol_size)
    decoder = decoder_factory.build()

    # Allocate some data to encode. Just for fun - fill the data with random
    # data
    data_in = bytearray(os.urandom(encoder.block_size()))
    data_in = bytes(data_in)

    # Assign the data buffer to the encoder so that we may start
    # to produce encoded symbols from it
    encoder.set_symbols(data_in)

    while not decoder.is_complete():

        # Encode a packet into the payload buffer
        packet = encoder.encode()

        if encoder.has_trace():
            print("Trace encoder:")
            encoder.trace()

        # Here we "simulate" a packet loss of approximately 50%
        # by dropping half of the encoded packets.
        # When running this example you will notice that the initial
        # symbols are received systematically (i.e. uncoded). After
        # sending all symbols once uncoded, the encoder will switch
        # to full coding, in which case you will see the full encoding
        # vectors being sent and received.
        if random.choice([True, False]):
            continue

        # Pass that packet to the decoder
        decoder.decode(packet)
        if decoder.has_trace():
            filter_function = lambda zone: zone in [
                "decoder_state",
                "input_symbol_coefficients"]

            print("Trace decoder:")
            # Try to run without a filter to see the full amount of
            # output produced by the trace function. You can then
            # modify the filter to only view the information you are
            # interested in.
            decoder.filtered_trace(filter_function)

    # The decoder is complete, now copy the symbols from the decoder
    data_out = decoder.copy_symbols()

    # Check we properly decoded the data
    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unexpected failure to decode please file a bug report :)")

if __name__ == "__main__":
    main()
