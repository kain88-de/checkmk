
##################################################################################
# Sorting
##################################################################################

# return -1, if r1 < r2, 0 if they are equal, 1 otherwise
def cmp_atoms(s1, s2):
    if s1 < s2:
        return -1
    elif s1 == s2:
        return 0
    else:
        return 1

def cmp_state_equiv(r):
    if r["service_has_been_checked"] == 0:
	return -1
    s = r["service_state"]
    if s <= 1:
	return s
    else:
	return 5 - s # swap crit and unknown

def cmp_svc_states(r1, r2):
    return cmp_atoms(cmp_state_equiv(r1), cmp_state_equiv(r2))
   
def cmp_simple_string(column, r1, r2):
    v1, v2 = r1[column], r2[column]
    c = cmp_atoms(v1.lower(), v2.lower())
    # force a strict order in case of equal spelling but different
    # case!
    if c == 0:
	return cmp_atoms(v1, v2)
    else:
	return c
    
def cmp_simple_number(column, r1, r2):
    return cmp_atoms(r1[column], r2[column])
    
multisite_sorters["svcstate"] = {
    "title"   : "Service state",
    "table"   : "services",
    "columns" : ["service_state", "service_has_been_checked"],
    "cmp"     : cmp_svc_states
}

def cmp_site_host(r1, r2):
    c = cmp_atoms(r1["site"], r2["site"])
    if c != 0:
	return c
    else:
	return cmp_simple_string("host_name", r1, r2)

multisite_sorters["site_host"] = {
    "title"   : "Host",
    "table"   : "hosts",
    "columns" : ["site", "host_name" ],
    "cmp"     : cmp_site_host
}

def declare_simple_sorter(name, title, table, column, func):
    multisite_sorters[name] = {
	"title"   : title,
	"table"   : table,
	"columns" : [ column ],
        "cmp"     : lambda r1, r2: func(column, r1, r2)
    }


#                      name         title                   table       column                   sortfunction
declare_simple_sorter("svcdescr",  "Service description",   "services", "service_description",   cmp_simple_string)
declare_simple_sorter("svcoutput", "Service plugin output", "services", "service_plugin_output", cmp_simple_string)
declare_simple_sorter("site",      "Site",                   None,      "site",                  cmp_simple_string)

