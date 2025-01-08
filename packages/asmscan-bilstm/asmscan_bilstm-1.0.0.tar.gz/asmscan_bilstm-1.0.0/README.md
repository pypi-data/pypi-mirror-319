# ASMscan-BiLSTM

![Python Version](https://img.shields.io/badge/python-3.11-306998?logo=python) ![GitHub License](https://img.shields.io/github/license/jakub-galazka/asmscan-lstm)

Bidirectional LSTM model for detection of amyloid signaling motifs (ASMs).

## Installation

```bash
pip install asmscan-bilstm
```

## Usage

```python
from asmscan.bilstm import BiLSTM

aa_seqs = [
    "MEGRASGSARIYQAGGDQYIEESDGYRADG",
    "VSLRAGAHDGGRIYQAVGDQYIYEDGGRAGASLREDGYQRIYAGASIYEA",
    "HASGHGRVFQSAGDQHITEHAGHDG"
]

model = BiLSTM()
pred, frags = model.predict(aa_seqs)
```

The `predict()` method of the BiLSTM model position-wise averages the predictions of the 6 cross-validation models, and then applies max-pooling over the sequence length. Sequences are processed using a&nbsp;window of size 40 and a&nbsp;step of 1.

## References

ASMscan-BiLSTM model is part of the [ASMscan](https://github.com/wdyrka-pwr/ASMscan) project:

* Not yet published.

ASMscan project is an extension of the ASMs analysis conducted with the [PCFG-CM](https://git.e-science.pl/wdyrka/pcfg-cm) model:

* W. Dyrka, M. Gąsior-Głogowska, M. Szefczyk, N. Szulc, "Searching for universal model of amyloid signaling motifs using probabilistic context-free grammars", *BMC Bioinformatics*, 22, 222, 2021.

* W. Dyrka, M. Pyzik, F. Coste, H. Talibart, "Estimating probabilistic context-free grammars for proteins using contact map constraints", *PeerJ*, 7, e6559, 2019.
