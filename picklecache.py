#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pickle Cache."""


import os
import pickle


class PickleCache(object):
    """A simple file-backed caching engine using Pickle."""

    def __init__(self, file_path='datastore.pkl', autosync=False):
        """PickleCache class constructor.

        Args:
            file_path(str): The file path. Defaults to 'datastore.pkl'.
            autosync(bool): Defaults to False.

        Returns:
            Instatiated class

        Examples:
            >>> cacher = PickleCache()
            >>> kprint cacher._PickleCache__file_path
            'datastore.pkl'
            >>> print cacher._PickleCache__file_object
            None
            >>> print cacher._PickleCache__data
            {}

        Atributes:
            __file_path(str):i.Pseudo-private assigned the constructor
                variable file_path.
            __data(dict): ii.Pseudo-private, instantiated as an empty
                dictionary object.
            autosync(bool): Non-private attribute sets data autosync.
            """
        self.__file_path = file_path
        self.__data = {}
        self.autosync = autosync
        self.load()

    def __setitem__(self, key, value):
        """Adds key and its value to dictionary and writes cache to file.

        Args:
            key(mixed): A dictionary key.
            value(mixed): The value of the key.

        Returns:
            Dictionary: Updated with key and its value.

        Examples:
            >>> pcache = PickleCache()
            >>> pcache['test'] = 'hello'
            >>> print pcache._PickleCache__data['test']
            'hello'
        """
        self.__data[key] = value
        if self.autosync is True:
            self.flush()

    def __len__(self):
        """Returns length of the dictionary.

        Args:
            None

        Returns:
            Int: The the lenght of the dictionary.

        Examples:
            >>> pcache = PickleCache()
            >>> pcache['test'] = 'hello'
            >>> len(pcache)
            1
        """
        datalength = len(self.__data)
        return datalength

    def __getitem__(self, key):
        """Gets dictionary item.

        Args:
            key(mixed): The dictionary key to lookup.

        Returns:
            Mixed: The value of the key.

        Examples:
            >>> pcache = PickleCache()
            >>> pcache['test'] = 'hello'
            >>> print pcache['test']
            'hello'

        Raises:
            myerrors: TypeError or KeyError if key lookup errors.
        """
        try:
            if self.__data[key]:
                return self.__data[key]
        except (TypeError, KeyError) as myerrors:
            raise myerrors

    def __delitem__(self, key):
        """Deletes key in dictionary.

        Args:
            key(mixed): The dictionary key to delete.

        Returns:
            None.

        Examples:
            >>> pcache = PickleCache()
            >>> pcache['test'] = 'hello'
            >>> print len(pcache)
            1
            >>> del pcache['test']
            >>> print len(pcache)
            0
        """
        if self.__data[key]:
            del self.__data[key]
        if self.autosync is True:
            self.flush()

    def load(self):
        """Checks for existance of file and loads it.

        Args:
            None:

        Returns:
            The contents of the file.

        Examples:
            >>> import pickle
            >>> fh = open('datastore.pkl', 'w')
            >>> pickle.dump({'foo': 'bar'}, fh)
            >>> fh.close()
            >>> pcache = PickleCache('datastore.pkl')
            >>> print pcache['foo']
            'bar'
        """
        if os.path.exists(self.__file_path) \
           and os.path.getsize(self.__file_path) > 0:
            readfile = open(self.__file_path, 'r')
            self.__data = pickle.load(readfile)
            readfile.close()

    def flush(self):
        """Saves cache to file.

        Args:
            None.

        Returns:
            None.

        Examples:
            >>> pcache = PickleCache()
            >>> pcache['foo'] = 'bar'
            >>> pcache.flush()
            >>> fhandler = open(pcache._PickleCache__file_path, 'r')
            >>> data = pickle.load(fhandler)
            >>> print data
            {'foo': 'bar'}
        """
        writefile = open(self.__file_path, 'w')
        pickle.dump(self.__data, writefile)
        writefile.close()
