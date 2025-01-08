import copy
import gzip
import pickle
import re
import traceback

from xbase_util.packet_util import filter_visible_chars
from xbase_util.pcap_util import reassemble_tcp, reassemble_session

if __name__ == '__main__':
    # req = EsReq("http://127.0.0.1:9200")
    # exp=build_es_expression(size="1",
    #                     start_time=None,
    #                     end_time=None,
    #                     arkime_expression='id == 250106-lKoC7T_SwbNAe4xDQQx7KTOd')
    # session=req.search(body=exp,index="arkime_sessions3-*").json()['hits']['hits'][0]
    # packetPos=session['_source']['packetPos']
    # stream,packet_objs=process_session_id_disk_simple(id=session['_id'], node=session['_source']['node'],
    #                                packet_pos=packetPos, esdb=EsDb(req, multiprocessing.Manager()),
    #                                pcap_path_prefix="origin")
    #
    # with open('stream.pkl', 'wb') as f:
    #     pickle.dump(stream, f)
    # with open('packet_objs.pkl', 'wb') as f:
    #     pickle.dump(packet_objs, f)

    with open('stream.pkl', 'rb') as f:
        stream = pickle.load(f)
    with open('packet_objs.pkl', 'rb') as f:
        packet_objs = pickle.load(f)
    skey = f"10.28.7.16:54398"
    reassemble_tcp_res = reassemble_tcp(packet_objs, skey)
    all_packets = reassemble_session(reassemble_tcp_res, skey)
    time_period = [( abs(item['res_time']-item['req_time'])) for item in
                   all_packets if item['res_time'] != 0 and item['req_time'] != 0]
    print(all_packets)
