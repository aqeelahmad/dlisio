import numpy as np
import pytest

import dlisio
from dlisio.plumbing import linkage

def test_frame_getitem(DWL206):
    frame = DWL206.object('FRAME', '2000T', 2, 0)
    curves = frame.curves()

    expected = [16677259.0, 852606.0, 2233.0, 852606.0]

    assert list(curves[0]) == expected

    assert curves['TIME'][0] == 16677259.0
    assert curves[0]['TIME'] == 16677259.0

    assert curves['TDEP'][0] == 852606.0
    assert curves[0]['TDEP'] == 852606.0

def makeframe():
    frame = dlisio.plumbing.Frame()
    frame.name = 'MAINFRAME'
    frame.origin = 0
    frame.copynumber = 0

    time0 = dlisio.plumbing.Channel()
    time0.name = 'TIME'
    time0.origin = 0
    time0.copynumber = 0
    time0.dimension = [1]
    time0.reprc = 2 # f4
    time0.frame = frame

    tdep = dlisio.plumbing.Channel()
    tdep.name = 'TDEP'
    tdep.origin = 0
    tdep.copynumber = 0
    tdep.dimension = [2]
    tdep.reprc = 13 # i2
    tdep.frame = frame

    time1 = dlisio.plumbing.Channel()
    time1.name = 'TIME'
    time1.origin = 1
    time1.copynumber = 0
    time1.dimension = [1]
    time1.reprc = 13 # i2
    time1.frame = frame

    frame.channels = [time0, tdep, time1]

    return frame

def test_duplicated_mnemonics_gets_unique_labels():
    frame = makeframe()
    assert 'fDDD' == frame.fmtstr()
    assert ('TIME.0.0', 'TDEP', 'TIME.1.0') == frame.dtype.names

def test_duplicated_mnemonics_dtype_supports_buffer_protocol():
    # Getting a buffer from a numpy array adds a :name: field after the label
    # name, and forbids the presence of :. Unfortunately, the full visible
    # (non-whitespace) ascii set is legal for the RP66 IDENT type, so in theory
    # it's possible that a similar mnemonic can be legally present.
    #
    # In practice, this is unlikely to be a problem. By default, dlisio uses
    # the full stop (.) as a separator, but for particularly nasty files this
    # would collide with a different channel mnemonic in the same frame. A
    # possible fix could be to use a blank character for mnemonic-origin-copy
    # separation, or lowercase letters (which are not supposed to be a part of
    # the IDENT type, but dlisio imposes no such restriction)
    #
    # https://github.com/equinor/dlisio/pull/97
    frame = makeframe()
    _ = memoryview(np.zeros(1, dtype = frame.dtype))

def test_duplicated_channels(assert_log):
    frame = makeframe()
    channel = frame.channels[0]
    frame.channels = [channel, channel]
    with pytest.raises(ValueError):
        frame.dtype.names
    assert_log("duplicated mnemonics")

    frame.link([frame, channel])
    assert_log("belongs to frame")

def test_instance_dtype_fmt():
    frame = makeframe()
    frame.dtype_fmt = 'x-{:s} {:d}~{:d}'

    # fmtstr is unchanged
    assert 'fDDD' == frame.fmtstr()
    assert ('x-TIME 0~0', 'TDEP', 'x-TIME 1~0') == frame.dtype.names

@pytest.mark.parametrize('fmt', [
    ("x-{:d}.{:s}.{:d}"),
    ("x-{:s}.{:d}.{:d}.{:d}"),
])
def test_instance_dtype_wrong_fmt(fmt, assert_log):
    frame = makeframe()

    frame.dtype_fmt = fmt
    with pytest.raises(Exception):
        frame.dtype.names
    assert_log("rich label")

def test_class_dtype_fmt():
    original = dlisio.plumbing.Frame.dtype_format

    try:
        # change dtype before the object itself is constructed, so it
        dlisio.plumbing.Frame.dtype_format = 'x-{:s} {:d}~{:d}'
        frame = makeframe()
        assert 'fDDD' == frame.fmtstr()
        assert ('x-TIME 0~0', 'TDEP', 'x-TIME 1~0') == frame.dtype.names

    finally:
        # even if the test fails, make sure the format string is reset to its
        # default, to not interfere with other tests
        dlisio.plumbing.Frame.dtype_format = original

def test_channel_curves():
    ch1 = dlisio.plumbing.Channel()
    ch1.dimension = [5]
    ch1.reprc = 11

    ch2 = dlisio.plumbing.Channel()
    ch2.dimension = [2, 2]
    ch2.reprc = 3

    ch3 = dlisio.plumbing.Channel()
    ch3.dimension = [4, 2]
    ch3.reprc = 26

    ch4 = dlisio.plumbing.Channel()
    ch4.dimension = [1]
    ch4.reprc = 17

    ch5 = dlisio.plumbing.Channel()
    ch5.dimension = [2, 3, 1]
    ch5.reprc = 12

    frame = dlisio.plumbing.Frame()
    frame.channels = [ch1, ch2, ch3, ch4, ch5]

    pre_fmt, ch_fmt, post_fmt = frame.fmtstrchannel(ch3)
    assert pre_fmt  == "CCCCCbbbb"
    assert ch_fmt   == "qqqqqqqq"
    assert post_fmt == "Ldddddd"

def test_channel_no_dimension(assert_log):
    ch = dlisio.plumbing.Channel()
    ch.name = 'CH'
    ch.origin = 0
    ch.copynumber = 0
    ch.reprc = 17

    with pytest.raises(ValueError) as exc:
        ch.fmtstr()
    assert "channel.dimension is unvalid" in str(exc.value)

    ch.dimension = [1]
    assert ch.fmtstr() == "L"

def test_not_a_link(assert_log):
    f = dlisio.plumbing.Frame()
    f.linkage = dict(f.linkage)
    f.linkage['notlink'] = linkage.objref
    f.refs["notlink"] = "not a link"

    f.link([f])
    assert_log("wrong linkage")

def test_wrong_linkage(assert_log):
    f = dlisio.plumbing.Frame()
    f.linkage = dict(f.linkage)
    f.linkage['wrong reference'] = "wrong reference"
    f.refs['wrong reference'] = dlisio.core.obname(3, 4, "aa");

    f.link([f])
    assert_log("wrong linkage")

def test_frame_index():
    frame = makeframe()
    frame.index_type = 'DECREASING'

    assert frame.index == frame.channels[0]

def test_frame_noindex(assert_info):
    frame = makeframe()

    assert frame.index is None
    assert_info('There is no index channel')

def test_frame_nochannels_no_index(assert_info):
    frame = dlisio.plumbing.Frame()
    frame.index_type = 'DECREASING'

    assert frame.index == None
    assert_info('There is no index channel')

def test_channel_index():
    frame = makeframe()
    frame.index_type = 'DECREASING'

    index   = frame.channels[0]
    channel = frame.channels[1]

    assert channel.index == index

def test_channel_is_index(assert_info):
    frame = makeframe()
    frame.index_type = 'DECREASING'
    channel = frame.channels[0]

    assert channel.index == channel
    assert_info('This channel is an index channel')

def test_channel_noindex(assert_info):
    frame = makeframe()
    channel = frame.channels[0]

    assert channel.index is None
    assert_info('There is no index channel')
