from pathlib import Path as _Path
from typing import List

import _kaldi_native_io
from _kaldi_native_io import (
    CompressionMethod,
    HtkHeader,
    MatrixShape,
    WaveData,
    WaveInfo,
)
from _kaldi_native_io import _DoubleMatrix as DoubleMatrix
from _kaldi_native_io import _DoubleVector as DoubleVector
from _kaldi_native_io import _FloatMatrix as FloatMatrix
from _kaldi_native_io import _FloatVector as FloatVector
from _kaldi_native_io import read_blob, read_wave, read_wave_info

from .table_types import (
    BoolWriter,
    CompressedMatrixWriter,
    DoubleMatrixWriter,
    DoubleVectorWriter,
    DoubleWriter,
    FloatMatrixWriter,
    FloatPairVectorWriter,
    FloatVectorWriter,
    FloatWriter,
    GaussPostWriter,
    HtkMatrixWriter,
    Int8VectorWriter,
    Int32PairVectorWriter,
    Int32VectorVectorWriter,
    Int32VectorWriter,
    BlobWriter,
    Int32Writer,
    PosteriorWriter,
    RandomAccessBoolReader,
    RandomAccessBlobReader,
    RandomAccessDoubleMatrixReader,
    RandomAccessDoubleReader,
    RandomAccessDoubleVectorReader,
    RandomAccessFloatMatrixReader,
    RandomAccessFloatPairVectorReader,
    RandomAccessFloatReader,
    RandomAccessFloatVectorReader,
    RandomAccessGaussPostReader,
    RandomAccessHtkMatrixReader,
    RandomAccessInt8VectorReader,
    RandomAccessInt32PairVectorReader,
    RandomAccessInt32Reader,
    RandomAccessInt32VectorReader,
    RandomAccessInt32VectorVectorReader,
    RandomAccessMatrixShapeReader,
    RandomAccessPosteriorReader,
    RandomAccessTokenReader,
    RandomAccessTokenVectorReader,
    RandomAccessWaveInfoReader,
    RandomAccessWaveReader,
    SequentialBoolReader,
    SequentialDoubleMatrixReader,
    SequentialDoubleReader,
    SequentialDoubleVectorReader,
    SequentialFloatMatrixReader,
    SequentialFloatPairVectorReader,
    SequentialFloatReader,
    SequentialFloatVectorReader,
    SequentialGaussPostReader,
    SequentialHtkMatrixReader,
    SequentialInt8VectorReader,
    SequentialInt32PairVectorReader,
    SequentialInt32Reader,
    SequentialBlobReader,
    SequentialInt32VectorReader,
    SequentialInt32VectorVectorReader,
    SequentialMatrixShapeReader,
    SequentialPosteriorReader,
    SequentialTokenReader,
    SequentialTokenVectorReader,
    SequentialWaveInfoReader,
    SequentialWaveReader,
    TokenVectorWriter,
    TokenWriter,
    WaveWriter,
)

cmake_prefix_path = _Path(__file__).parent / "share" / "cmake"
del _Path


def read_int32_vector(rxfilename: str) -> List[int]:
    """Read a vector of int32 from an rxfilename"""
    return _kaldi_native_io.read_int32_vector(rxfilename)


def read_int8_vector(rxfilename: str) -> List[int]:
    """Read a vector of int8 from an rxfilename"""
    return _kaldi_native_io.read_int8_vector(rxfilename)
__version__ = '1.22.1'
