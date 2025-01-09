from itertools import groupby
from typing import Tuple, Callable, Iterator, MutableMapping

from vizitig.index import load_kmer_index
from vizitig.info import get_graph
from vizitig.index import temporary_kmerindex
from vizitig.search import fetch_nodes_by_kmers, fetch_nodes_by_dna
from vizitig.types import Color, Kmer, Metadata, DNA
from vizitig.utils import SubLog
from vizitig.env_var import VIZITIG_NO_TMP_INDEX
from vizitig.utils import vizitig_logger as logger
from vizitig.types import SubseqData


def tag_graph_from_nodes_id(name: str, nodes_id: set[int], metadata: Metadata):
    """Add the metadata to the nodes in nodes_id. Associate to each nodes either description if description is a str or
    to the ith node of nodes_id the description[i].
    In the latter case, it will zip both iterator that are assumed to be the same size.
    The metadata should be set either with a key or an offset of a key of already existing metadata.
    Data mush hold in RAM.
    """
    G = get_graph(name)

    G.helper.pragma_fk = False

    logger.info(f"Found {len(nodes_id)} nodes to tag")

    with SubLog("tagging"):
        d = {metadata: None}
        G.add_node_data_from(
            [(nid, d) for nid in nodes_id],
        )


def tag_graph_from_dna(name: str, dnas: Callable[[], Iterator[DNA]], color: Color):
    """Add the metadata to all unitigs nodes speciefied by the list of kmer in kmer_list.
    The metadata should be set either with a key or an offset of a key of already existing metadata.
    """
    logger.info(f"Tagging nodes with {color}")
    with SubLog("fetch_by_kmers"):
        nodes_id = set(fetch_nodes_by_dna(name, dnas))
    with SubLog("tag_from_id"):
        tag_graph_from_nodes_id(name, nodes_id, color)


def tag_graph_from_kmer(
    name: str, kmer_list: Iterator[Kmer] | Callable[[], Iterator[Kmer]], color: Color
):
    """Add the metadata to all unitigs nodes speciefied by the list of kmer in kmer_list.
    The metadata should be set either with a key or an offset of a key of already existing metadata.
    """
    logger.info(f"Tagging nodes with {color}")
    with SubLog("fetch_by_kmers"):
        nodes_id = set(fetch_nodes_by_kmers(name, kmer_list))
    with SubLog("tag_from_id"):
        tag_graph_from_nodes_id(name, nodes_id, color)


def bulk_annotate_graph(gname: str, generator: Callable[[], Iterator[Tuple[DNA, int]]]):
    Graph = get_graph(gname)
    k = Graph.metadata.k
    index = load_kmer_index(gname)

    def pos_int_generator():
        yield from ((dna, -i) for dna, i in generator())

    if VIZITIG_NO_TMP_INDEX:
        it_dna = pos_int_generator()
        it_kmer = (
            (kmer, meta) for dna, meta in it_dna for kmer in dna.enum_canonical_kmer(k)
        )
        res_join = groupby(sorted(index.join(it_kmer)), key=lambda e: e[0])
    else:
        tmp_index = temporary_kmerindex(
            pos_int_generator, k, index_type=index.index_type.__name__
        )
        res_join = groupby(sorted(index.join_index(tmp_index)), key=lambda e: e[0])
        # sorted could probably be removed in index join is in sorted order.

    # This could be done by chunk, if too big to hold in RAM
    graph_annotations = []
    for inode, E in res_join:
        d: MutableMapping[SubseqData, None] = {}
        for _, m in E:
            meta = Graph.metadata.decoder(-m)
            if meta.gene:
                s = SubseqData(
                    id=meta.gene, type="Gene", start=0, stop=0, list_attr=meta.list_attr
                )
                s = Graph.metadata.add_metadata(s)
                d[s] = None
            d[meta] = None
        graph_annotations.append((inode, d))
    Graph.add_node_data_from(graph_annotations)
