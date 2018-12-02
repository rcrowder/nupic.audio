#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run inner ear model from [Zilany2014]_.

"""
from __future__ import division, print_function, absolute_import

from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import thorns as th
import cochlea
import resampy


data_dir = "free-spoken-digit-dataset/recordings"

def show_wav_info(aname, a):
    print("Array", aname)
    print("shape:", a.shape)
    print("dtype:", a.dtype)
    print("min, max:", a.min(), a.max())
    print()


def read_wav_file(file_name):
    _, data = wavfile.read(data_dir + file_name)
    # show_wav_info(file_name, data)
    return data


def main():

    data = read_wav_file('/0_jackson_0.wav')

    minval = 0
    maxval = 20.0
    fs = 100e3  # Hz

    # Upsample using resampy. Not as good as scikit.resample is but is useable
    # and certainly better than scipy.signal.resample!
    # http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html
    data = resampy.resample(data, 8000, fs)

    # The Zilany2014 model requires the data to be in dB SPL.
    # To do this the auditory threshold is used as the reference
    # sound pressure, i.e. p0 = 20 µPa
    # Desired level of the output signal in dB SPL set to 50
    data = cochlea.set_dbspl(data, 50)

    pad = np.zeros(int(10e-3 * fs))
    data = np.concatenate((data, pad))

    # Run model
    anf = cochlea.run_zilany2014(
        data,
        fs,                     # [100e3, 500e3]
        anf_num=(10, 10, 10),    # (HSR#, MSR#, LSR#)
        cf=(125, 20000, 100),   # (min_cf, max_cf, num_cf)
        seed=0,
        powerlaw='approximate',
        species='human',
    )

    # Accumulate spike trains
    anf_acc = th.accumulate(anf, keep=['cf', 'duration'])
    anf_acc.sort_values('cf', ascending=False, inplace=True)

    # Plot auditory nerve response
    _, ax = plt.subplots(2, 1)
    th.plot_signal(
        signal=data,
        fs=fs,
        ax=ax[0]
    )
    th.plot_neurogram(
        anf_acc,
        fs,
        ax=ax[1]
    )
    plt.show()



if __name__ == "__main__":
    main()
