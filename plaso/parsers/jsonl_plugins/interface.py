# -*- coding: utf-8 -*-
"""Interface for JSON-L parser plugins."""

import abc
import json
import os

from dfvfs.helpers import text_file

from plaso.parsers import plugins


class JSONLPlugin(plugins.BasePlugin):
  """This is an abstract class from which plugins should be based.

  The following are the attributes and methods expected to be overridden by
  a JSON-L parser plugin.
  """

  NAME = 'jsonl_plugin'

  def _GetJSONValue(self, json_dict, name, default_value=None):
    """Retrieves a value from a JSON dict.

    Args:
      json_dict (dict): JSON dictionary.
      name (str): name of the value to retrieve.
      default_value (Optional[object]): default value to return if the value
          is not set or empty.

    Returns:
      object: value of the JSON log entry or None if not set.
    """
    json_value = json_dict.get(name, default_value)
    if json_value == '':
      json_value = default_value
    return json_value

  @abc.abstractmethod
  def _ParseRecord(self, parser_mediator, json_dict):
    """Parses a JSON-L log record structure and produces events.

    This function takes as an input a parsed JSON dictionary and produces
    events.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      json_dict (dict): JSON dictionary of the log record.
    """

  @abc.abstractmethod
  def CheckRequiredFormat(self, json_dict):
    """Check if the log record has the minimal structure required by the plugin.

    Args:
      json_dict (dict): JSON dictionary of the log record.

    Returns:
      bool: True if this is the correct parser, False otherwise.
    """

  # pylint: disable=arguments-differ
  def Process(self, parser_mediator, file_object=None, **kwargs):
    """Extracts events from a JSON-L log file.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      file_object (Optional[dfvfs.FileIO]): a file-like object.
    """
    # This will raise if unhandled keyword arguments are passed.
    super(JSONLPlugin, self).Process(parser_mediator)

    file_object.seek(0, os.SEEK_SET)
    text_file_object = text_file.TextFile(file_object)

    # TODO: add support to handle corrupt lines like text parser.
    for line in text_file_object:
      json_dict = json.loads(line)
      self._ParseRecord(parser_mediator, json_dict)
