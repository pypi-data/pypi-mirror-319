# vi: set softtabstop=2 ts=2 sw=2 expandtab:
# pylint: disable=redefined-builtin,invalid-name,missing-module-docstring
# TODO: Remove above exceptions.  At some point rename `type` parameter which
#       will allow us to remove redefined-builtin and invalid-name for
#       builtin_type

from mergeconf import exceptions

# aliasing this allows the use of a parameter `type`, for which I can't find a
# reasonable replacement (like `klass` for `class`)
builtin_type = type

class MergeConfItem:
  """
  Basic configuration item and base class for more complex types.
  """
  def _set_value_appropriately(self, value):
    if value is None:
      self._value = value
    elif self._choices is not None:
      if value in self._choices:
        self._value = self._type(value)
      else:
        # TODO: define the section :(
        raise exceptions.InvalidChoice("TODO: implement", self._key, self._choices, value)
    elif self._type == bool:
      if isinstance(value, bool):
        self._value = value
      else:
        self._value = value.lower() in ['true', 'yes', '1']
    else:
      self._value = self._type(value)

  def __init__(self, key, value=None, type=None, choices=None,
      mandatory=False, cli=False, description=None):
    """
    Create a configuration item.

    Arguments:
      key: Configuration item's key.
      value: Current value
      type: Item data type.  Must be one of bool, int, float or str.  If not
        specified, will be autodetected.
      choices: List of possible values.
      mandatory: Item must have configured value for configuration to be valid.
      cli: Include item in command-line argument parsing.
      description (str): Short descriptive text that may appear in usage text
        or sample configurations
    """
    if type and type not in [bool, int, float, str]:
      raise exceptions.UnsupportedType(type)
    if not type:
      if value is None:
        type = str
      else:
        type = builtin_type(value)
        if type not in [bool, int, float, str]:
          type = str

    self._key = key
    self._type = type
    self._choices = choices
    self._mandatory = mandatory
    self._cli = cli
    self._description = description

    self._set_value_appropriately(value)

  # pylint: disable=missing-function-docstring
  @property
  def key(self):
    return self._key

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self._set_value_appropriately(value)

  @property
  def type(self):
    return self._type

  @property
  def choices(self):
    return self._choices

  @property
  def mandatory(self):
    return self._mandatory

  @property
  def cli(self):
    return self._cli

  @property
  def description(self):
    return self._description
