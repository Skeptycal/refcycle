# Copyright 2013 Mark Dickinson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import gc
import inspect

__all__ = [
    'ObjectGraph', 'cycles_created_by', 'snapshot', 'disable_gc',
    'objects_reachable_from', 'garbage',
    'key_cycles',
]

from refcycle.object_graph import ObjectGraph


@contextlib.contextmanager
def disable_gc():
    """
    Context manager to temporarily disable garbage collection.

    """
    if gc.isenabled():
        gc.disable()
        try:
            yield
        finally:
            gc.enable()
    else:
        # Nothing to do.
        yield


@contextlib.contextmanager
def set_gc_flags(flags):
    old_flags = gc.get_debug()
    gc.set_debug(flags)
    try:
        yield
    finally:
        gc.set_debug(old_flags)


def cycles_created_by(callable):
    """
    Return graph of cyclic garbage created by the given callable.

    Return an ObjectGraph representing those objects generated by the given
    callable that can't be collected by Python's usual reference-count based
    garbage collection.

    This includes objects that will eventually be collected by the cyclic
    garbage collector, as well as genuinely unreachable objects that will
    never be collected.

    `callable` should be a callable that takes no arguments; its return
    value (if any) will be ignored.

    """
    with disable_gc():
        gc.collect()
        with set_gc_flags(gc.DEBUG_SAVEALL):
            callable()
            new_object_count = gc.collect()
            if new_object_count:
                objects = gc.garbage[-new_object_count:]
                del gc.garbage[-new_object_count:]
            else:
                objects = []
            return ObjectGraph(objects)


def garbage():
    """
    Collect garbage and return a graph based on collected garbage.

    Collected elements are removed from gc.garbage, but are still kept alive by
    the references in the ObjectGraph.  Deleting the ObjectGraph and doing
    another gc.collect will remove those objects for good.

    """
    with disable_gc(), set_gc_flags(gc.DEBUG_SAVEALL):
        collected_count = gc.collect()
        if collected_count:
            objects = gc.garbage[-collected_count:]
            del gc.garbage[-collected_count:]
        else:
            objects = []
        return ObjectGraph(objects)


def snapshot():
    """
    Return the graph of all currently gc-tracked objects.

    Excludes the returned ObjectGraph and objects owned by it.

    """
    all_objects = gc.get_objects()
    this_frame = inspect.currentframe()
    graph = ObjectGraph(
        [
            obj for obj in all_objects
            if obj is not this_frame
            if obj is not all_objects
        ]
    )
    del this_frame, all_objects
    return graph


def objects_reachable_from(obj):
    """
    Return graph of all objects reachable from the given one.

    """
    found = {}
    # Depth-first search.
    to_process = [obj]
    while to_process:
        obj = to_process.pop()
        obj_id = id(obj)
        found[obj_id] = obj
        refs = gc.get_referents(obj)
        for ref in refs:
            if id(ref) not in found:
                to_process.append(ref)
    return ObjectGraph(found.values())


def _is_orphan(scc, graph):
    """
    Return False iff the given scc is reachable from elsewhere.

    """
    return all(
        p in scc for v in scc
        for p in graph.parents(v))


def key_cycles():
    """
    Collect cyclic garbage, and return the strongly connected
    components that were keeping the garbage alive.

    """
    graph = garbage()
    sccs = graph.strongly_connected_components()
    return [
        scc for scc in sccs if _is_orphan(scc, graph)
    ]
