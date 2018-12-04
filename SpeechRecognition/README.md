# Speech Recognition

The aim of this example is:

- Test the ability of NuPIC unsupervised learning, along with a supervised trained SDR Classifier, to recognize spoken digits.
- To test traditional Fourier Analysis approaches to encoding, with simulated biological spike encoding.
- To compare recognition with existing ML Neural Networks, particularly and _importantly_ with regards to added background noise and other speakers.

A number of existing ML based examples can be used to contrast with this example, such as:
1. https://towardsdatascience.com/speech-classification-using-neural-networks-the-basics-e5b08d6928b7
1. https://towardsdatascience.com/audio-classification-using-fastai-and-on-the-fly-frequency-transforms-4dbe1b540f89

## Encoding

### [Frequency Encoding](https://github.com/marionleborgne/frequency-encoder)

As described in the Frequency Encoder [README.md](https://github.com/marionleborgne/frequency-encoder/blob/master/README.md) file;  

> The FrequencyEncoder encodes a time series chunk (or any 1D array of numeric values) 
by taking the power spectrum of the signal and discretizing it. The discretization is 
done by slicing the frequency axis of the power spectrum into bins. The maximum amplitude 
of the power spectrum in this frequency bin is encoded by a [Scalar Encoder](http://nupic.docs.numenta.org/1.0.3/api/algorithms/encoders.html#scalar-encoders). 

To make use of the Frequency Encoder, continuous signal data needs to be broken into 
chunks. Achieving this is done by extracting a contiguous chunk of input data and applying 
an appropriate window function to this chunk of data. The next contiguous chunk of 
input data is extracted with appropriate overlay with the previous chunk. These chunks of 
data can then be passed into the Frequency Encoder to obtain a sparse distributed 
representation (SDR) for each chunk.

<img src="./docs/windowing.png" alt="Hann window function" style="width: 400px;"/>

The Frequency Encoder uses a short time fourier transform (STFT). Care 
must be taken when determining how big a chunk of input data is (number of data samples),
and the parameters used for the STFT and Frequency Encoder (specifically the Scalar Encoder).

> One of the pitfalls of the STFT is that it has a fixed resolution. The width of
 the windowing function relates to how the signal is represented - it determines 
 whether there is good frequency resolution (frequency components close together 
 can be separated) or good time resolution (the time at which frequencies change).
 A wide window gives better frequency resolution but poor time resolution.
 A narrower window gives good time resolution but poor frequency resolution.

Source: https://en.wikipedia.org/wiki/Short-time_Fourier_transform

The Free Spoken Digit Dataset has been recorded using a 8000 Hz sampling rate, and each 
mono sample is typically around 1 second long. Each sample can be up-sampled using a Python
package called [resampy](https://github.com/bmcfee/resampy). Other resampling methods 
can be used in Python. Refer to this blog post for an overview: 
http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html

### [Spike Encoding](https://github.com/mrkrd/cochlea)

For spike encoding a Python package called [cochlea](https://github.com/mrkrd/cochlea) can be used.

> cochlea is a collection of inner ear models. All models are easily accessible as 
 Python functions. They take sound signal as input and return spike trains of the 
 auditory nerve fibers (ANF).

From the three inner ear models implemented in the cochlea package, one compelling 
reason to use spike encoding is:

> The ability of auditory models to code speech is already very elaborate, all three 
outperform classical Mel-frequency cepstral features (MFCC), the “gold standard” of 
automatic speech recognition.

As mentioned in the accompanying research paper [1], the Zilany model (2014) [2,3] is 
the most feature rich. And:

> Offset adaptation is only implemented in Zilany’s phenomenological model. Offset 
adaptation can be very important for further neuronal processing. Therefore, if modeled
ANF spike trains are used as input to neurons in the brainstem (or even higher), one 
should consider the Zilany et al. (2014) model 

One advantage of using the cochlea Zilany model implementation, over the Frequency Encoder, 
is that an entire sample can be input to it. No need to segment/chunk the data and apply 
a window function. One disadvantage is that the Zilany model has a lower frequency bound 
of 125 Hz.

<img src="./docs/sine_spike_encoding.png" alt="Chirp spike encoding" style="width: 400px;"/>

1. Rudnicki M., Schoppe O., Isik M., Völk F. and Hemmert W. (2015). Modeling auditory 
coding: from sound to spikes. Cell and Tissue Research, Springer Nature, 361, 159—175. 
http://link.springer.com/article/10.1007/s00441-015-2202-z

1. Zilany MSA, Bruce IC, Nelson PC, Carney LH (2009) A phenomenological model of the 
synapse between the inner hair cell and auditory nerve: Long-term adaptation with 
power-law dynamics. J Acoust Soc Am 126(5):2390

1. Zilany MSA, Bruce IC, Carney LH (2014) Updated parameters and expanded simulation 
options for a model of the auditory periphery. J Acoust Soc Am 135(1):283–286

## Network setup

### Spatial Pooler

### Temporal Memory

### SDR Classifier

http://hopding.com/sdr-classifier

> The purpose of the SDR Classifier is identical to that of the older CLA Classifier: 
learn associations between a given state of the Temporal Memory at time t, and the 
value that is to be fed into the Encoder at time t+n (where n is the number of steps 
into the future you want to predict. t+1, t+5, t+2 - or all three!). You can also 
think of it as mapping activation patterns (vector of Temporal Memory’s active cells) 
to probability distributions (for the possible encoder buckets).

## Training

### Classifier training

## Testing

Background noise data:  
http://soundbible.com/641-Urban-Traffic.html  
http://soundbible.com/1265-Shopping-Mall-Ambiance.html  

## Dataset and Python packages

Dependant python packages can be install using the following command:

```sh
pip install -r requirements.txt
```

Dependant Git repositories can be cloned using the following Python script:

```sh
python RepoClone.py
```

**Note**: RepoClone.py uses [GitPython](https://github.com/gitpython-developers/GitPython). It requires [Git](https://git-scm.com/) being installed on the system, and accessible via the system's PATH.

### Repository cloning (RepoClone.py)

#### Free spoken digit dataset (FFDD)

A free audio dataset of spoken digits. Think MNIST for audio. -  https://github.com/Jakobovski/free-spoken-digit-dataset

#### Frequency Encoder

A custom frequency encoder for the HTM. - https://github.com/marionleborgne/frequency-encoder

#### ISOLET dataset

The database consists of 7800 spoken letters, 2 productions of each letter by 150 speakers - https://archive.ics.uci.edu/ml/datasets/isolet