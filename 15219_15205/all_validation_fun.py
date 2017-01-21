import re

def valid_name(fname):
    regex_fname=re.compile('[a-zA-Z]+$')
    fname_obj = regex_fname.match(fname)
    if fname_obj is not None:
        return True
    else:
        return False

def valid_age(age):
    age = str(age)
    regex_age=re.compile('^(0?[1-9]|[1-9][0-9])$')
    match_age = regex_age.match(age)
    if match_age is not None:
        return True
    else:
        return False


def valid_street_add(street_name):
    regex_street=re.compile('^[a-z|A-Z][0-9]+\,([\s]|[a-zA-Z]+)*$')
    match_street = regex_street.match(street_name)
    if match_street is not None:
            return True
    else:
        return False

def valid_state(st_name):
    regex_state = re.compile('^[A-Z|a-z]{1,3}$')
    match_state = regex_state.match(st_name)
    if match_state is not None:
        return True
    else :
        return False

def valid_city(city_nm):
    regex_city=re.compile('[a-z|A-Z]+')
    match_city = regex_city.match(city_nm)
    if match_city is not None:
        return True
    else:
        return False

def valid_code(pstl_code):
    regex_code = re.compile('^[1-9][0-9]{5}')
    match_code = regex_code.match(pstl_code)
    if match_code is not None:
        return True
    return False


def valid_mb_number(mb_num):
    regex_mob = re.compile('\d{10}$')
    obj_mb_no = regex_mob.match(mb_num)
    if obj_mb_no is not None:
        return True
    else:
        return False


def valid_phn_number(land_line_num):
    regex_phno = re.compile('\d{3}[-]\d{8}$')
    obj_phno = regex_phno.match(land_line_num)
    if obj_phno is not None:
        return True
    else:
        return False



