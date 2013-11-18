import unittest

from refcycle.annotated_graph import (
    AnnotatedEdge,
    AnnotatedGraph,
    AnnotatedVertex,
)


class TestAnnotatedGraph(unittest.TestCase):
    def test_simple_graph_construction(self):
        # Direct construction of a simple annotated graph.
        v1 = AnnotatedVertex(id=0, annotation="vertex 1")
        v2 = AnnotatedVertex(id=1, annotation="vertex 2")
        e1 = AnnotatedEdge(
            id=3,
            annotation="edge from vertex 1 to vertex 2",
            tail=0,
            head=1,
        )
        graph = AnnotatedGraph(
            vertices=[v1, v2],
            edges=[e1],
        )
        self.assertEqual(len(graph.vertices), 2)
        self.assertItemsEqual(graph.children(v1), [v2])
        self.assertItemsEqual(graph.parents(v2), [v1])

    def test_strongly_connected_components(self):
        # Direct construction of a simple annotated graph.
        graph = AnnotatedGraph(
            vertices=[
                AnnotatedVertex(id=0, annotation="vertex 1"),
                AnnotatedVertex(id=1, annotation="vertex 2"),
            ],
            edges=[
                AnnotatedEdge(
                    id=3,
                    annotation="from 1 to 2",
                    head=0,
                    tail=1,
                ),
            ],
        )
        self.assertEqual(len(graph.vertices), 2)
        sccs = graph.strongly_connected_components()
        self.assertEqual(len(sccs), 2)
        self.assertEqual(len(sccs[0]), 1)
        self.assertEqual(len(sccs[1]), 1)
        self.assertIsInstance(sccs[0], AnnotatedGraph)
        self.assertIsInstance(sccs[1], AnnotatedGraph)

    def test_export_json(self):
        graph = AnnotatedGraph(
            vertices=[
                AnnotatedVertex(id=0, annotation="vertex 1"),
                AnnotatedVertex(id=1, annotation="vertex 2"),
            ],
            edges=[
                AnnotatedEdge(
                    id=3,
                    annotation="from 1 to 2",
                    head=0,
                    tail=1,
                ),
            ],
        )
        json = graph.export_json()
        reconstructed = AnnotatedGraph.from_json(json)
        self.assertIsInstance(reconstructed, AnnotatedGraph)
        self.assertEqual(len(reconstructed), 2)

        for vertex in graph:
            self.assertIn(vertex, reconstructed)
        for vertex in reconstructed:
            self.assertIn(vertex, graph)