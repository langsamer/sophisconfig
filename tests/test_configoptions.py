import pytest
from sophconf.configoptions import *


def test_initialize():
    c = Config()
    assert c


def test_attributes_option1():
    """you can create new attributes on a Config object"""
    c = Config()
    c._create_option('verbose', value=True)
    assert hasattr(c, 'verbose')
    assert c.verbose


def test_attributes_option2():
    """you can change the value of a user-defined attribute on a Config object
    """
    c = Config()
    c._create_option('verbose', value=True)
    c.verbose = False
    assert hasattr(c, 'verbose')
    assert not c.verbose


def test_attributes_section1():
    """you can create a new section on a Config object"""
    c = Config()
    c._create_section('Simulation')


def test_attributes_section2():
    """you can create a new section on a Config object, and that is again a Config object"""
    c = Config()
    c._create_section('Simulation')
    assert hasattr(c, 'Simulation')
    assert isinstance(c.Simulation, Config)


def test_attributes_section3():
    """when you create a new section on a Config object, you can pass a dictionary to initialize it"""
    c = Config()
    c._create_section('Simulation', {'option1': 123})
    assert c.Simulation.option1 == 123


def test_seeding_dict1():
    """you can initialize a Config object from a dictionary"""
    d = {'option1': 5}
    c = Config(d)
    assert c.option1 == 5


def test_seeding_dict2():
    """you can initialize a Config object with nested dictionaries
    to create sections and subsections"""
    d = {'option1': 5, 'section1': {'option2': True, 'section3': {}}}
    c = Config(d)
    assert isinstance(c.section1, Config)


def test_seeding_dict3():
    """you can initialize a Config object with nested dictionaries
    to create sections and subsections"""
    d = {'option1': 5, 'section1': {'option2': True, 'section3': {}}}
    c = Config(d)
    s1 = c.section1
    assert s1.option2
    assert isinstance(s1.section3, Config)


def test_suboptions_assignable():
    """options in sections or subsections can be assigned to"""
    d = {'option1': 5, 'section1': {'option2': True, 'section3': {}}}
    c = Config(d)
    c.section1.option2 = 7
    assert c.section1.option2 == 7


def test_subsections_not_overwritable():
    """a section cannot be overwritten"""
    d = {'option1': 5, 'section1': {'option2': True, 'section3': {}}}
    c = Config(d)
    with pytest.raises(TypeError):
        c.section1 = 77
        assert isinstance(c.section1, Config)


def test_nonexistent_option_raises_keyerror():
    """trying to read an option that does not exist raises a KeyError"""
    d = {'option1': 99}
    c = Config(d)
    with pytest.raises(KeyError) as exc:
        x = c.option2
        assert 'option2' in str(exc)


def test_nonexistent_section_raises_keyerror():
    """trying to read from a section that does not exist raises a KeyError"""
    d = {'option1': 99}
    c = Config(d)
    with pytest.raises(KeyError) as exc:
        x = c.section2.option3
        assert 'section2' in str(exc)


def test_can_create_new_option():
    """you can (by default) add new options by simply assigning to them"""
    c = Config()
    c.option1 = 8
    assert c.option1 == 8


def test_prevent_creating_options():
    """you can prevent users from creating new options in a Config object"""
    c = Config(protected=True)
    with pytest.raises(TypeError):
        c.option1 = 8


def test_config_can_have_types():
    """if you create your Config object with typed=True, it will require each option
    update to match the original type of the option"""
    d = {'option1': 99}
    c = Config(d, typed=True)
    with pytest.raises(TypeError):
        c.option1 = "Hello"