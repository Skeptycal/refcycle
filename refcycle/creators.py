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
"""
Top-level functions for creating :class:`~refcycle.object_graph.ObjectGraph`
instances.

"""
import gc
import inspect

from refcycle.gc_utils import restore_gc_state
from refcycle.object_graph import ObjectGraph


def cycles_created_by(callable):
    """
    Return graph of cyclic garbage created by the given callable.

    Return an :class:`~refcycle.object_graph.ObjectGraph` representing those
    objects generated by the given callable that can't be collected by Python's
    usual reference-count based garbage collection.

    This includes objects that will eventually be collected by the cyclic
    garbage collector, as well as genuinely unreachable objects that will
    never be collected.

    `callable` should be a callable that takes no arguments; its return
    value (if any) will be ignored.

    """
    with restore_gc_state():
        gc.disable()
        gc.collect()
        gc.set_debug(gc.DEBUG_SAVEALL)
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
    Collect garbage and return an :class:`~refcycle.object_graph.ObjectGraph`
    based on collected garbage.

    The collected elements are removed from ``gc.garbage``, but are still kept
    alive by the references in the graph.  Deleting the
    :class:`~refcycle.object_graph.ObjectGraph` instance and doing another
    ``gc.collect`` will remove those objects for good.

    """
    with restore_gc_state():
        gc.disable()
        gc.set_debug(gc.DEBUG_SAVEALL)
        collected_count = gc.collect()
        if collected_count:
            objects = gc.garbage[-collected_count:]
            del gc.garbage[-collected_count:]
        else:
            objects = []
        return ObjectGraph(objects)


def objects_reachable_from(obj):
    """
    Return graph of objects reachable from *obj* via ``gc.get_referrers``.

    Returns an :class:`~refcycle.object_graph.ObjectGraph` object holding all
    objects reachable from the given one by following the output of
    ``gc.get_referrers``.  Note that unlike the
    :func:`~refcycle.creators.snapshot` function, the output graph may
    include non-gc-tracked objects.

    """
    # Depth-first search.
    found = ObjectGraph.vertex_set()
    to_process = [obj]
    while to_process:
        obj = to_process.pop()
        found.add(obj)
        for referent in gc.get_referents(obj):
            if referent not in found:
                to_process.append(referent)
    return ObjectGraph(found)


def snapshot():
    """Return the graph of all currently gc-tracked objects.

    Excludes the returned :class:`~refcycle.object_graph.ObjectGraph` and
    objects owned by it.

    Note that a subsequent call to :func:`~refcycle.creators.snapshot` will
    capture all of the objects owned by this snapshot.  The
    :meth:`~refcycle.object_graph.ObjectGraph.owned_objects` method may be
    helpful when excluding these objects from consideration.

    """
    all_objects = gc.get_objects()
    this_frame = inspect.currentframe()
    selected_objects = []
    for obj in all_objects:
        if obj is not this_frame:
            selected_objects.append(obj)
    graph = ObjectGraph(selected_objects)
    del this_frame, all_objects, selected_objects, obj
    return graph