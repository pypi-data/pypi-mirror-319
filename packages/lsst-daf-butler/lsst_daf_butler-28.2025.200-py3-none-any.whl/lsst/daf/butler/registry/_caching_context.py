# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

__all__ = ["CachingContext"]

from ._collection_record_cache import CollectionRecordCache
from ._collection_summary_cache import CollectionSummaryCache


class CachingContext:
    """Collection of caches for various types of records retrieved from
    database.

    Notes
    -----
    Caching is usually disabled for most of the record types, but it can be
    explicitly and temporarily enabled in some context (e.g. quantum graph
    building) using Registry method. This class is a collection of cache
    instances which will be `None` when caching is disabled. Instance of this
    class is passed to the relevant managers that can use it to query or
    populate caches when caching is enabled.
    """

    def __init__(self) -> None:
        self._collection_records: CollectionRecordCache | None = None
        self._collection_summaries: CollectionSummaryCache | None = None
        self._depth = 0

    @property
    def is_enabled(self) -> bool:
        return self._collection_records is not None

    def _enable(self) -> None:
        """Enable caches.

        For use only by RegistryManagerInstances, which is the single point
        of entry for enabling and disabling the caches.
        """
        if self._depth == 0:
            self._collection_records = CollectionRecordCache()
            self._collection_summaries = CollectionSummaryCache()
        self._depth += 1

    def _disable(self) -> None:
        """Disable caches.

        For use only by RegistryManagerInstances, which is the single point
        of entry for enabling and disabling the caches.
        """
        if self._depth == 1:
            self._collection_records = None
            self._collection_summaries = None
            self._depth = 0
        elif self._depth > 1:
            self._depth -= 1
        else:
            raise AssertionError("Bad caching context management detected.")

    @property
    def collection_records(self) -> CollectionRecordCache | None:
        """Cache for collection records (`CollectionRecordCache`)."""
        return self._collection_records

    @property
    def collection_summaries(self) -> CollectionSummaryCache | None:
        """Cache for collection summary records (`CollectionSummaryCache`)."""
        return self._collection_summaries
