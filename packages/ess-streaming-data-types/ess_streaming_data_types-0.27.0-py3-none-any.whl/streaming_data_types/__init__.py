from streaming_data_types._version import version
from streaming_data_types.action_response_answ import deserialise_answ, serialise_answ
from streaming_data_types.alarm_al00 import deserialise_al00, serialise_al00
from streaming_data_types.area_detector_ad00 import deserialise_ad00, serialise_ad00
from streaming_data_types.area_detector_ADAr import deserialise_ADAr, serialise_ADAr
from streaming_data_types.area_detector_NDAr import deserialise_ndar, serialise_ndar
from streaming_data_types.array_1d_se00 import deserialise_se00, serialise_se00
from streaming_data_types.dataarray_da00 import deserialise_da00, serialise_da00
from streaming_data_types.epics_connection_ep01 import deserialise_ep01, serialise_ep01
from streaming_data_types.epics_connection_info_ep00 import (
    deserialise_ep00,
    serialise_ep00,
)
from streaming_data_types.eventdata_an44 import deserialise_an44, serialise_an44
from streaming_data_types.eventdata_ev42 import deserialise_ev42, serialise_ev42
from streaming_data_types.eventdata_ev43 import deserialise_ev43, serialise_ev43
from streaming_data_types.eventdata_ev44 import deserialise_ev44, serialise_ev44
from streaming_data_types.finished_writing_wrdn import deserialise_wrdn, serialise_wrdn
from streaming_data_types.forwarder_config_update_fc00 import (
    deserialise_fc00,
    serialise_fc00,
)
from streaming_data_types.forwarder_config_update_rf5k import (
    deserialise_rf5k,
    serialise_rf5k,
)
from streaming_data_types.histogram_hs00 import deserialise_hs00, serialise_hs00
from streaming_data_types.histogram_hs01 import deserialise_hs01, serialise_hs01
from streaming_data_types.json_json import deserialise_json, serialise_json
from streaming_data_types.logdata_f142 import deserialise_f142, serialise_f142
from streaming_data_types.logdata_f144 import deserialise_f144, serialise_f144
from streaming_data_types.nicos_cache_ns10 import deserialise_ns10, serialise_ns10
from streaming_data_types.run_start_pl72 import deserialise_pl72, serialise_pl72
from streaming_data_types.run_stop_6s4t import deserialise_6s4t, serialise_6s4t
from streaming_data_types.sample_environment_senv import (
    deserialise_senv,
    serialise_senv,
)
from streaming_data_types.status_x5f2 import deserialise_x5f2, serialise_x5f2
from streaming_data_types.timestamps_tdct import deserialise_tdct, serialise_tdct

__version__ = version

SERIALISERS = {
    "an44": serialise_an44,
    "ev42": serialise_ev42,
    "ev43": serialise_ev43,
    "ev44": serialise_ev44,
    "hs00": serialise_hs00,
    "hs01": serialise_hs01,
    "f142": serialise_f142,
    "f144": serialise_f144,
    "ns10": serialise_ns10,
    "pl72": serialise_pl72,
    "6s4t": serialise_6s4t,
    "x5f2": serialise_x5f2,
    "ep00": serialise_ep00,
    "ep01": serialise_ep01,
    "tdct": serialise_tdct,
    "rf5k": serialise_rf5k,
    "fc00": serialise_fc00,
    "answ": serialise_answ,
    "wrdn": serialise_wrdn,
    "NDAr": serialise_ndar,
    "senv": serialise_senv,
    "se00": serialise_se00,
    "ADAr": serialise_ADAr,
    "al00": serialise_al00,
    "json": serialise_json,
    "ad00": serialise_ad00,
    "da00": serialise_da00,
}


DESERIALISERS = {
    "an44": deserialise_an44,
    "ev42": deserialise_ev42,
    "ev43": deserialise_ev43,
    "ev44": deserialise_ev44,
    "hs00": deserialise_hs00,
    "hs01": deserialise_hs01,
    "f142": deserialise_f142,
    "f144": deserialise_f144,
    "ns10": deserialise_ns10,
    "pl72": deserialise_pl72,
    "6s4t": deserialise_6s4t,
    "x5f2": deserialise_x5f2,
    "ep00": deserialise_ep00,
    "ep01": deserialise_ep01,
    "tdct": deserialise_tdct,
    "rf5k": deserialise_rf5k,
    "fc00": deserialise_fc00,
    "answ": deserialise_answ,
    "wrdn": deserialise_wrdn,
    "NDAr": deserialise_ndar,
    "senv": deserialise_senv,
    "se00": deserialise_se00,
    "ADAr": deserialise_ADAr,
    "al00": deserialise_al00,
    "json": deserialise_json,
    "ad00": deserialise_ad00,
    "da00": deserialise_da00,
}
