=========
 Changes
=========


4.5.0 (2025-01-08)
==================

- Make the modules in ``nti.zodb.btrees.family64LargeBuckets``
  properly provide the set operations like ``multiunion``. Previously,
  due to an error in ``BTrees``, these were not available.


4.4.1 (2024-12-24)
==================

- Make ``IZODBZConfigProvider`` correctly extend ``IZODBConfigProvider``.


4.4.0 (2024-12-24)
==================

- Make ``provideDatabases`` properly return the mapping of all
  installed databases.
- Make ``provideDatabases`` and related APIs detect and collapse equal
  databases into a single component. This is handy for aliases, for
  example while evolving a code base.


4.3.0 (2024-12-23)
==================

- Add a series of interfaces and APIs supporting database
  configuration and registration for use during process startup.
  See `nti.zodb.config_providers.provideDatabases`.


4.2.0 (2024-12-02)
==================

- Add a case-insensitive but case-preserving BTreeContainer and
  BTreeFolder.


1.4.0 (2024-11-08)
==================

- Drop support for Python < 3.10.
- Use native namespace packages.


1.3.0 (2021-04-01)
==================

- Add support for Python 3.9.

- The ZODB activity log monitor now has separate thresholds for loads
  and stores, in addition to the total combined threshold; exceeding
  any threshold will trigger logging.

  The thresholds have all been set to 10, but can be configured with
  environment variables.

  See `issue 11 <https://github.com/NextThought/nti.zodb/issues/11>`_.

1.2.0 (2020-08-06)
==================

- Add a BTree "family" object to ``nti.zodb.btrees`` that uses larger
  bucket sizes. See `issue 8 <https://github.com/NextThought/nti.zodb/issues/8>`_.

- All numeric minmax objects implement the same interface, providing
  the ``increment`` method. See `issue 7
  <https://github.com/NextThought/nti.zodb/issues/7>`_.

- The merging counter does the right thing when reset to zero by two
  conflicting transactions. See `issue 6
  <https://github.com/NextThought/nti.zodb/issues/6>`_.

1.1.0 (2020-07-15)
==================

- Add support for Python 3.7 and 3.8.

- Loading this package's configuration no longer marks
  ``persistent.list.PersistentList`` as implementing the deprecated
  interface ``zope.interface.common.sequence.ISequence``. This
  conflicts with a strict resolution order. Prefer
  ``zope.interface.common.collections.ISequence`` or its mutable
  descendent, which ``PersistentList`` already implements.

- Rework ``nti.zodb.activitylog`` to be faster. Client code may need
  to adapt for best efficiency.

- The monitors in ``nti.zodb.activitylog`` now include information
  about the ZODB connection pool. See `issue 4
  <https://github.com/NextThought/nti.zodb/issues/4>`_.

- The log monitor now has a configurable threshold, defaulting to at
  least one load or store. See `issue 3
  <https://github.com/NextThought/nti.zodb/issues/3>`_.

1.0.0 (2017-06-08)
==================

- First PyPI release.
- Add support for Python 3.
- Remove nti.zodb.common. See
  https://github.com/NextThought/nti.zodb/issues/1.
  ``ZlibClientStorageURIResolver`` will no longer try to set a ``var``
  directory to store persistent cache files automatically.
- ``CopyingWeakRef`` now implements ``ICachingWeakRef``.
